from typing import List
from sqlalchemy.orm import Session
from app.modules.leaderboard.repository import LeaderboardRepository
from app.modules.leaderboard.schemas import LeaderboardResponse, LeaderboardEntryResponse
from app.shared.errors import ValidationError


class LeaderboardService:
    """Contains business logic for Leaderboard leagues and period standings."""

    VALID_PERIODS = {"weekly", "monthly", "all_time"}

    def __init__(self, db: Session):
        self.db = db
        self.repository = LeaderboardRepository(db)

    def get_leaderboard(self, period: str = "weekly") -> LeaderboardResponse:
        period_clean = period.lower().strip() if period else "weekly"
        if period_clean not in self.VALID_PERIODS:
            raise ValidationError(
                f"Invalid period parameter '{period}'. Allowed values: {', '.join(sorted(self.VALID_PERIODS))}."
            )

        raw_entries = self.repository.get_entries_by_period(period_clean)
        entries: List[LeaderboardEntryResponse] = []

        for idx, entry in enumerate(raw_entries, start=1):
            user = entry.user
            entries.append(
                LeaderboardEntryResponse(
                    rank=entry.rank or idx,
                    user_id=entry.user_id,
                    username=user.username if user else "unknown",
                    display_name=user.display_name if user else "Unknown Learner",
                    avatar=user.avatar if user else None,
                    xp=entry.xp,
                )
            )

        return LeaderboardResponse(period=period_clean, entries=entries)
