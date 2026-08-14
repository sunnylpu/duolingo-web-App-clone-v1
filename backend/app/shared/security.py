"""
JWT security utilities for the Duolingo Clone API.

Design principles (Phase 36.1):
  - JWTs include jti (unique token ID), iss (issuer), aud (audience) in addition to sub/role/exp/iat
  - Token revocation is keyed by jti — efficient, small, storage-backend-agnostic
  - TokenBlocklist interface is designed for a future Redis/shared-store backend;
    the in-process Dict is explicitly documented as single-replica only.
  - In Kubernetes (Phase 39), swap the in-process Dict for a Redis adapter
    without changing any calling code.
"""

import uuid
import jwt
import bcrypt
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
    Storage-independent revoked-token registry keyed by jti (JWT ID).

    Architecture note:
      This implementation stores revoked jti values in a process-local Dict.
      It is intentionally designed with a clean interface so the Dict can be
      replaced by a Redis adapter in Phase 39 (Kubernetes) without changing
      any calling code:

          token_blocklist = RedisTokenBlocklist(redis_client)

      Until then, this correctly provides revocation for single-replica
      deployments and development/test environments.
    """

    def __init__(self):
        # jti -> exp_timestamp (UTC epoch float)
        self._revoked_jtis: Dict[str, float] = {}
        self._lock = threading.Lock()

    def revoke_jti(self, jti: str, exp_timestamp: Optional[float] = None) -> None:
        """Mark a token JTI as revoked until its expiration time."""
        if not jti:
            return
        if exp_timestamp is None:
            exp_timestamp = (
                datetime.datetime.now(datetime.timezone.utc)
                + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            ).timestamp()

        with self._lock:
            self._revoked_jtis[jti] = exp_timestamp
            self._prune()

    def is_jti_revoked(self, jti: str) -> bool:
        """Returns True if the given jti has been revoked and is still within its TTL."""
        if not jti:
            return False
        with self._lock:
            return jti in self._revoked_jtis

    def _prune(self) -> None:
        """Remove expired entries to bound memory usage."""
        now = datetime.datetime.now(datetime.timezone.utc).timestamp()
        self._revoked_jtis = {
            jti: exp for jti, exp in self._revoked_jtis.items() if exp > now
        }

    def clear(self) -> None:
        """Reset for test isolation."""
        with self._lock:
            self._revoked_jtis.clear()

    # ---------------------------------------------------------------------------
    # Legacy compatibility shim — kept so existing call sites still work.
    # Internally delegates to jti-based revocation by decoding the token first.
    # ---------------------------------------------------------------------------
    def revoke(self, token: str, exp_timestamp: Optional[float] = None) -> None:
        """Revoke a raw JWT by extracting and revoking its jti claim."""
        if not token:
            return
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=["HS256"],
                options={"verify_exp": False},
                audience=settings.JWT_AUDIENCE,
                issuer=settings.JWT_ISSUER,
            )
            jti = payload.get("jti")
            exp = exp_timestamp or payload.get("exp")
            if jti:
                self.revoke_jti(jti, exp)
        except Exception:
            # If token cannot be decoded (expired, malformed) nothing to revoke
            pass

    def is_revoked(self, token: str) -> bool:
        """Check revocation for a raw JWT via its jti claim (legacy shim)."""
        if not token:
            return False
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=["HS256"],
                options={"verify_exp": False},
                audience=settings.JWT_AUDIENCE,
                issuer=settings.JWT_ISSUER,
            )
            jti = payload.get("jti")
            return self.is_jti_revoked(jti) if jti else False
        except Exception:
            return False


# Global singleton instance
# Replace with RedisTokenBlocklist(redis_client) in Phase 39 Kubernetes deployment
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


def create_access_token(
    user_id: str,
    role: str = "user",
    expires_delta: Optional[datetime.timedelta] = None,
) -> str:
    """
    Generates a signed JWT access token with OWASP-recommended claims:
      sub  — subject (user ID)
      role — RBAC role
      jti  — unique token ID for server-side revocation
      iss  — issuer (this API service)
      aud  — audience (intended client)
      iat  — issued at
      exp  — expiration
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    expire = now + (expires_delta or datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    payload = {
        "sub": user_id,
        "role": role,
        "jti": str(uuid.uuid4()),
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
        "iat": now,
        "exp": expire,
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")


def decode_access_token(token: str) -> dict:
    """
    Decodes and validates a JWT access token.

    Validates:
      - Signature (HS256 + secret)
      - Expiration (exp)
      - Issuer (iss == JWT_ISSUER)
      - Audience (aud == JWT_AUDIENCE)
      - jti not in revocation blocklist
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=["HS256"],
            audience=settings.JWT_AUDIENCE,
            issuer=settings.JWT_ISSUER,
        )
    except jwt.ExpiredSignatureError:
        raise UnauthorizedError("Authentication token has expired.", code="SESSION_EXPIRED")
    except jwt.InvalidAudienceError:
        raise UnauthorizedError("Invalid token audience.", code="AUTHENTICATION_REQUIRED")
    except jwt.InvalidIssuerError:
        raise UnauthorizedError("Invalid token issuer.", code="AUTHENTICATION_REQUIRED")
    except jwt.InvalidTokenError:
        raise UnauthorizedError("Invalid authentication token.", code="AUTHENTICATION_REQUIRED")

    # Check jti revocation after successful decode
    jti = payload.get("jti")
    if jti and token_blocklist.is_jti_revoked(jti):
        raise UnauthorizedError("Session has been revoked.", code="SESSION_REVOKED")

    return payload


def get_current_user(
    request: Request,
    header_token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> UserModel:
    """
    FastAPI security dependency resolving current authenticated learner identity.
    Token extraction order:
      1. 'Authorization: Bearer <token>' header
      2. HttpOnly 'auth_token' cookie
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

    # Strict development fallback — never active in production
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
