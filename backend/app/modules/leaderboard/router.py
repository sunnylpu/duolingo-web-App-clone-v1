from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.shared.database import get_db
from app.modules.leaderboard.service import LeaderboardService
from app.modules.leaderboard.schemas import LeaderboardResponse

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])


def get_leaderboard_service(db: Session = Depends(get_db)) -> LeaderboardService:
    return LeaderboardService(db)


@router.get("", response_model=LeaderboardResponse, summary="Get leaderboard standings")
def get_leaderboard(
    period: str = Query("weekly", description="Leaderboard period: weekly, monthly, all_time"),
    service: LeaderboardService = Depends(get_leaderboard_service),
):
    """Return ranked leaderboard standings for the specified period."""
    return service.get_leaderboard(period=period)
