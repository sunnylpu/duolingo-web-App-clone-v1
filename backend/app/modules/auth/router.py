from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from app.shared.database import get_db
from app.shared.security import get_current_user
from app.config import settings
from app.modules.auth.service import AuthService
from app.modules.auth.schemas import RegisterRequest, LoginRequest, AuthResponse
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
    hashes credentials securely, sets HttpOnly auth cookie, and returns access token.
    """
    svc = AuthService(db)
    res = svc.register(req)
    _set_auth_cookie(response, res.access_token)
    return res


@router.post("/login", response_model=AuthResponse, summary="Authenticate learner credentials")
def login_user(req: LoginRequest, request: Request, response: Response, db: Session = Depends(get_db)):
    """
    Authenticates user credentials against hashed password, establishes authenticated session,
    sets HttpOnly auth cookie, and returns signed access token.
    """
    client_ip = request.client.host if request.client else "127.0.0.1"
    svc = AuthService(db)
    res = svc.login(req, client_ip=client_ip)
    _set_auth_cookie(response, res.access_token)
    return res


@router.post("/logout", summary="Invalidate authenticated learner session")
def logout_user(response: Response):
    """
    Clears HttpOnly authentication cookie and logs out current learner session.
    """
    response.delete_cookie(key="auth_token", path="/")
    return {"status": "ok", "message": "Logged out successfully"}


@router.get("/me", response_model=UserResponse, summary="Get current authenticated user profile")
def get_me(current_user: UserModel = Depends(get_current_user)):
    """
    Returns profile information for current authenticated user.
    """
    return UserResponse.model_validate(current_user)
