import jwt
import bcrypt
import hashlib
import datetime
import threading
from typing import Optional, Dict
from fastapi import Request, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config import settings
from app.shared.database import get_db
from app.shared.errors import UnauthorizedError, ForbiddenError
from app.modules.user.models import UserModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/token", auto_error=False)


class TokenBlocklist:
    """
    In-memory thread-safe revoked token storage with TTL-based expiration.
    Guarantees true server-side invalidation upon logout.
    """

    def __init__(self):
        self._revoked_tokens: Dict[str, float] = {}  # token_hash -> exp_timestamp
        self._lock = threading.Lock()

    def revoke(self, token: str, exp_timestamp: Optional[float] = None) -> None:
        if not token:
            return
        if exp_timestamp is None:
            # Default to 24h expiration
            exp_timestamp = (
                datetime.datetime.now(datetime.timezone.utc)
                + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            ).timestamp()

        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        with self._lock:
            self._revoked_tokens[token_hash] = exp_timestamp
            self._prune()

    def is_revoked(self, token: str) -> bool:
        if not token:
            return False
        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        with self._lock:
            return token_hash in self._revoked_tokens

    def _prune(self) -> None:
        now = datetime.datetime.now(datetime.timezone.utc).timestamp()
        self._revoked_tokens = {
            k: exp for k, exp in self._revoked_tokens.items() if exp > now
        }

    def clear(self) -> None:
        with self._lock:
            self._revoked_tokens.clear()


# Global singleton instance
token_blocklist = TokenBlocklist()


def hash_password(password: str) -> str:
    """Hashes plaintext password using bcrypt."""
    pwd_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies plaintext password against hashed password."""
    if not hashed_password:
        return False
    try:
        pwd_bytes = plain_password.encode("utf-8")[:72]
        hash_bytes = hashed_password.encode("utf-8")
        return bcrypt.checkpw(pwd_bytes, hash_bytes)
    except Exception:
        return False


def create_access_token(user_id: str, role: str = "user", expires_delta: Optional[datetime.timedelta] = None) -> str:
    """Generates signed JWT access token."""
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    payload = {
        "sub": user_id,
        "role": role,
        "exp": expire,
        "iat": datetime.datetime.now(datetime.timezone.utc),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")


def decode_access_token(token: str) -> dict:
    """Decodes and validates JWT access token with revocation checking."""
    if token_blocklist.is_revoked(token):
        raise UnauthorizedError("Session has been revoked.", code="SESSION_REVOKED")

    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise UnauthorizedError("Authentication token has expired.", code="SESSION_EXPIRED")
    except jwt.InvalidTokenError:
        raise UnauthorizedError("Invalid authentication token.", code="AUTHENTICATION_REQUIRED")


def get_current_user(
    request: Request,
    header_token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> UserModel:
    """
    FastAPI security dependency resolving current authenticated learner identity.
    Token extraction order:
    1. HttpOnly 'auth_token' cookie
    2. 'Authorization: Bearer <token>' header
    """
    token = header_token or request.cookies.get("auth_token")

    if token:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedError("Invalid authentication token payload.", code="AUTHENTICATION_REQUIRED")

        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user or not user.is_active:
            raise UnauthorizedError("User account not found or inactive.", code="ACCOUNT_DISABLED")
        return user

    # Strict development fallback only if explicitly enabled
    if settings.APP_ENV == "development" and getattr(settings, "ALLOW_DEV_AUTH_BYPASS", False):
        demo_user = db.query(UserModel).filter(UserModel.id == "usr_demo").first()
        if demo_user:
            return demo_user

    raise UnauthorizedError("Authentication required.", code="AUTHENTICATION_REQUIRED")


def require_admin(current_user: UserModel = Depends(get_current_user)) -> UserModel:
    """
    FastAPI security dependency restricting endpoint access to admin users.
    """
    if current_user.role != "admin":
        raise ForbiddenError("Admin access privileges required.", code="FORBIDDEN")
    return current_user
