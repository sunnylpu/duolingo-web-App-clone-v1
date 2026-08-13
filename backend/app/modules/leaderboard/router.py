from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.shared.database import get_db
from app.shared.security import get_current_user
from app.modules.user.models import UserModel
from app.modules.leaderboard.service import LeaderboardService
from app.modules.leaderboard.schemas import LeaderboardResponse, UserRankResponse

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])


def get_leaderboard_service(db: Session = Depends(get_db)) -> LeaderboardService:
    return LeaderboardService(db)


@router.get("", response_model=LeaderboardResponse, summary="Get leaderboard standings")
def get_leaderboard(
    period: str = Query("weekly", description="Leaderboard period: weekly, monthly, all_time"),
    limit: int = Query(20, ge=1, le=100, description="Max records to return"),
    offset: int = Query(0, ge=0, description="Record offset"),
    current_user: UserModel = Depends(get_current_user),
    service: LeaderboardService = Depends(get_leaderboard_service),
):
    """Return ranked leaderboard standings for the specified period."""
    return service.get_leaderboard(
        period=period,
        limit=limit,
        offset=offset,
        current_user_id=current_user.id,
    )


@router.get("/me", response_model=UserRankResponse, summary="Get current user rank")
def get_current_user_rank(
    period: str = Query("weekly", description="Leaderboard period: weekly, monthly, all_time"),
    current_user: UserModel = Depends(get_current_user),
    service: LeaderboardService = Depends(get_leaderboard_service),
):
    """Return current user's rank, XP, and total participants for the specified period."""
    return service.get_current_user_rank(user_id=current_user.id, period=period)
