from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.leaderboard.models import LeaderboardEntryModel


class LeaderboardRepository:
    """Handles data persistence for Leaderboard rankings."""

    def __init__(self, db: Session):
        self.db = db

    def get_entries_by_period(
        self, period: str = "weekly", limit: int = 50
    ) -> List[LeaderboardEntryModel]:
        return (
            self.db.query(LeaderboardEntryModel)
            .filter(LeaderboardEntryModel.period == period)
            .order_by(LeaderboardEntryModel.rank.asc())
            .limit(limit)
            .all()
        )

    def create_or_update_entry(
        self,
        entry_id: str,
        user_id: str,
        period: str = "weekly",
        xp: int = 0,
        rank: int = 1,
    ) -> LeaderboardEntryModel:
        entry = (
            self.db.query(LeaderboardEntryModel)
            .filter(
                LeaderboardEntryModel.user_id == user_id,
                LeaderboardEntryModel.period == period,
            )
            .first()
        )
        if not entry:
            entry = LeaderboardEntryModel(
                id=entry_id,
                user_id=user_id,
                period=period,
                xp=xp,
                rank=rank,
            )
            self.db.add(entry)
        else:
            entry.xp = xp
            entry.rank = rank

        self.db.commit()
        self.db.refresh(entry)
        return entry
