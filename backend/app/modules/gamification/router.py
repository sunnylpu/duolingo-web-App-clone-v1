from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.shared.database import get_db
from app.shared.security import get_current_user
from app.modules.user.models import UserModel
from app.modules.gamification.service import GamificationService
from app.modules.gamification.schemas import (
    GamificationStatsResponse,
    AchievementResponse,
    UserAchievementResponse,
)

router = APIRouter(prefix="/gamification", tags=["Gamification"])
achievement_router = APIRouter(tags=["Achievements"])


def get_gamification_service(db: Session = Depends(get_db)) -> GamificationService:
    return GamificationService(db)


@router.get("/stats", response_model=GamificationStatsResponse, summary="Get user gamification stats")
def get_gamification_stats(
    current_user: UserModel = Depends(get_current_user),
    service: GamificationService = Depends(get_gamification_service),
):
    """Return total XP, streaks, hearts, gems, and daily progress for current demo user."""
    return service.get_user_stats(current_user)


@achievement_router.get("/achievements", response_model=List[AchievementResponse], summary="List all platform achievements")
def list_achievements(service: GamificationService = Depends(get_gamification_service)):
    """Return all available achievements in the platform."""
    return service.get_all_achievements()


@achievement_router.get("/users/me/achievements", response_model=List[UserAchievementResponse], summary="Get current user achievements")
def get_my_achievements(
    current_user: UserModel = Depends(get_current_user),
    service: GamificationService = Depends(get_gamification_service),
):
    """Return all achievements and whether the current demo learner has unlocked each one."""
    return service.get_user_achievements(current_user)
