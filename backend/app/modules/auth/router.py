from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from app.shared.database import get_db
from app.shared.security import get_current_user, token_blocklist, decode_access_token
from app.config import settings
from app.modules.auth.service import AuthService
from app.modules.auth.schemas import RegisterRequest, LoginRequest, AuthResponse, TokenResponse
from app.modules.user.schemas import UserResponse
from app.modules.user.models import UserModel

router = APIRouter(prefix="/auth", tags=["auth"])


def _set_auth_cookie(response: Response, access_token: str):
    """Utility setting HttpOnly, Secure, SameSite auth_token cookie."""
    is_prod = settings.APP_ENV == "production"
    response.set_cookie(
        key="auth_token",
        value=access_token,
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=is_prod,
        path="/",
    )


@router.post("/register", response_model=AuthResponse, summary="Register new learner account")
def register_user(req: RegisterRequest, response: Response, db: Session = Depends(get_db)):
    """
    Registers a new learner user, creates initial gamification stats,
    hashes credentials securely, sets HttpOnly auth cookie, and returns user profile.
    (Token is set exclusively via HttpOnly cookie for browser security).
    """
    svc = AuthService(db)
    user, access_token = svc.register(req)
    _set_auth_cookie(response, access_token)
    return AuthResponse(user=UserResponse.model_validate(user), status="authenticated")


@router.post("/login", response_model=AuthResponse, summary="Authenticate learner credentials")
def login_user(req: LoginRequest, request: Request, response: Response, db: Session = Depends(get_db)):
    """
    Authenticates user credentials against hashed password, establishes authenticated session,
    sets HttpOnly auth cookie, and returns user profile.
    """
    client_ip = request.client.host if request.client else "127.0.0.1"
    svc = AuthService(db)
    user, access_token = svc.login(req, client_ip=client_ip)
    _set_auth_cookie(response, access_token)
    return AuthResponse(user=UserResponse.model_validate(user), status="authenticated")


@router.post("/token", response_model=TokenResponse, summary="Get programmatic API token for CLI / API clients")
def get_api_token(req: LoginRequest, request: Request, db: Session = Depends(get_db)):
    """
    Programmatic endpoint for external API / CLI clients returning raw Bearer access token.
    """
    client_ip = request.client.host if request.client else "127.0.0.1"
    svc = AuthService(db)
    _, access_token = svc.login(req, client_ip=client_ip)
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )


@router.post("/logout", summary="Invalidate authenticated learner session")
def logout_user(request: Request, response: Response):
    """
    Revokes the active JWT's jti in the server-side blocklist and clears the HttpOnly cookie.
    Revocation is keyed by jti (unique token identifier) rather than the raw token string,
    making the blocklist small and ready for a shared-store backend (Phase 39 / Redis).
    """
    token = request.cookies.get("auth_token")
    if not token:
        auth_hdr = request.headers.get("authorization")
        if auth_hdr and auth_hdr.startswith("Bearer "):
            token = auth_hdr[7:]

    if token:
        try:
            payload = decode_access_token(token)
            jti = payload.get("jti")
            exp = payload.get("exp")
            if jti:
                token_blocklist.revoke_jti(jti, exp)
        except Exception:
            # If token is already expired/invalid, nothing to revoke
            pass

    response.delete_cookie(key="auth_token", path="/")
    return {"status": "ok", "message": "Logged out and session revoked successfully"}


@router.get("/me", response_model=UserResponse, summary="Get current authenticated user profile")
def get_me(current_user: UserModel = Depends(get_current_user)):
    """
    Returns profile information for current authenticated user.
    """
    return UserResponse.model_validate(current_user)
