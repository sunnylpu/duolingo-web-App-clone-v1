from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.shared.database import get_db
from app.shared.security import get_current_user
from app.modules.user.models import UserModel
from app.modules.gamification.service import GamificationService
from app.modules.gamification.schemas import (
    GamificationStatsResponse,
    DailyActivityResponse,
    AchievementResponse,
    UserAchievementResponse,
    PracticeExerciseResponse,
    PracticeSubmissionRequest,
    PracticeSubmissionResponse,
    HeartRefillResponse,
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
    """Return total XP, streaks, hearts, heart regeneration info, gems, and daily progress."""
    return service.get_user_stats(current_user)


@router.get("/daily", response_model=DailyActivityResponse, summary="Get today's activity and goal progress")
def get_today_activity(
    current_user: UserModel = Depends(get_current_user),
    service: GamificationService = Depends(get_gamification_service),
):
    """Return today's date, XP earned, lessons completed, and daily goal completion status."""
    return service.get_today_activity(current_user)


@router.get("/practice", response_model=PracticeExerciseResponse, summary="Get practice exercise for heart recovery")
def get_practice_exercise(
    current_user: UserModel = Depends(get_current_user),
    service: GamificationService = Depends(get_gamification_service),
):
    """Return a practice exercise item for recovering a heart."""
    return service.get_practice_exercise()


@router.post("/practice", response_model=PracticeSubmissionResponse, summary="Submit practice answer")
def submit_practice_answer(
    req: PracticeSubmissionRequest,
    current_user: UserModel = Depends(get_current_user),
    service: GamificationService = Depends(get_gamification_service),
):
    """Submit answer for practice exercise. If correct and not on cooldown, grants +1 heart."""
    return service.submit_practice_answer(
        user_id=current_user.id,
        exercise_id=req.exercise_id,
        answer=req.answer,
    )


@router.post("/hearts/refill", response_model=HeartRefillResponse, summary="Mock refill hearts")
def refill_hearts(
    current_user: UserModel = Depends(get_current_user),
    service: GamificationService = Depends(get_gamification_service),
):
    """Mock refill hearts to MAX_HEARTS instantly."""
    return service.refill_hearts(current_user.id)


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
