from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.shared.database import get_db
from app.shared.security import get_current_user
from app.modules.user.models import UserModel
from app.modules.user.repository import UserRepository
from app.modules.user.service import UserService
from app.modules.user.schemas import UserResponse, UserStatsResponse, UserProfileResponse

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repository = UserRepository(db)
    return UserService(repository=repository, db=db)


@router.get("/me", response_model=UserResponse, summary="Get current demo user profile")
def get_me(
    current_user: UserModel = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    """Return the profile information of the current active demo user."""
    return service.get_me(current_user)


@router.get("/me/stats", response_model=UserStatsResponse, summary="Get current demo user stats")
def get_me_stats(
    current_user: UserModel = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    """Return gamification statistics (XP, streak, hearts, gems) for current demo user."""
    return service.get_me_stats(current_user)


@router.get("/me/profile", response_model=UserProfileResponse, summary="Get aggregated learner profile dashboard")
def get_user_profile(
    current_user: UserModel = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    """Return aggregated learner profile dashboard including user identity, stats, and learning progress summary."""
    return service.get_user_profile(current_user)
