import jwt
import bcrypt
import datetime
from typing import Optional
from fastapi import Request, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config import settings
from app.shared.database import get_db
from app.shared.errors import UnauthorizedError, ForbiddenError
from app.modules.user.models import UserModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/login", auto_error=False)


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
    """Decodes and validates JWT access token."""
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
    token = request.cookies.get("auth_token") or header_token

    if token:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedError("Invalid authentication token payload.", code="AUTHENTICATION_REQUIRED")

        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user or not user.is_active:
            raise UnauthorizedError("User account not found or inactive.", code="ACCOUNT_DISABLED")
        return user

    # Development mode fallback to demo user for local test convenience
    if settings.APP_ENV == "development":
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
