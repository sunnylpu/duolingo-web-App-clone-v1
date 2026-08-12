from typing import List
from sqlalchemy.orm import Session
from app.modules.leaderboard.models import LeaderboardModel


class LeaderboardRepository:
    """Handles data persistence for the Leaderboard domain."""

    def __init__(self, db: Session):
        self.db = db

    def get_league_standings(self, league_name: str) -> List[LeaderboardModel]:
        return (
            self.db.query(LeaderboardModel)
            .filter(LeaderboardModel.league_name == league_name)
            .order_by(LeaderboardModel.weekly_xp.desc())
            .all()
        )
