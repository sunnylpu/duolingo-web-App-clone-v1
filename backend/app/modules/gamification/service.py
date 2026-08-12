from app.modules.gamification.repository import GamificationRepository
from app.modules.gamification.schemas import GamificationResponse


class GamificationService:
    """Contains business logic for Gamification metrics (XP, Streaks, Hearts)."""

    def __init__(self, repository: GamificationRepository):
        self.repository = repository

    def get_user_stats(self, user_id: str) -> GamificationResponse:
        return GamificationResponse(
            id="gmf_01",
            user_id=user_id,
            xp=0,
            streak_count=0,
            hearts=5,
            gems=500,
        )
