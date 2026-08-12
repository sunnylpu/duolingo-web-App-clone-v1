from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.shared.database import get_db
from app.modules.leaderboard.repository import LeaderboardRepository
from app.modules.leaderboard.service import LeaderboardService
from app.modules.leaderboard.schemas import LeaderboardResponse

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


def get_leaderboard_service(db: Session = Depends(get_db)) -> LeaderboardService:
    repository = LeaderboardRepository(db)
    return LeaderboardService(repository)


@router.get("", response_model=LeaderboardResponse)
def get_leaderboard(
    league: str = "Bronze",
    service: LeaderboardService = Depends(get_leaderboard_service),
):
    """Retrieve leaderboard standings (scaffolding)."""
    return service.get_leaderboard(league_name=league)
