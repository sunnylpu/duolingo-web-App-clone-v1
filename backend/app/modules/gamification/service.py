from typing import List
from sqlalchemy.orm import Session
from app.modules.gamification.repository import GamificationRepository
from app.modules.gamification.models import AchievementModel, UserAchievementModel
from app.modules.user.models import UserModel
from app.modules.gamification.schemas import (
    GamificationStatsResponse,
    AchievementResponse,
    UserAchievementResponse,
)
from app.shared.errors import NotFoundError


class GamificationService:
    """Contains business logic for Gamification metrics, Hearts, and Achievements."""

    def __init__(self, db: Session):
        self.db = db
        self.repository = GamificationRepository(db)

    def get_user_stats(self, current_user: UserModel) -> GamificationStatsResponse:
        stats = self.repository.get_user_stats(current_user.id)
        if not stats and current_user.stats:
            stats = current_user.stats

        if not stats:
            raise NotFoundError("Gamification statistics not found.")

        return GamificationStatsResponse.model_validate(stats)

    def deduct_heart(self, user_id: str) -> int:
        """Deducts 1 heart for an incorrect answer, ensuring hearts never drop below 0."""
        stats = self.repository.get_user_stats(user_id)
        if not stats:
            raise NotFoundError(f"Gamification stats for user '{user_id}' not found.")

        stats.hearts = max(stats.hearts - 1, 0)
        self.db.flush()
        return stats.hearts

    def award_lesson_xp(self, user_id: str, xp_amount: int) -> int:
        """Awards fixed lesson XP reward to user_stats.total_xp safely."""
        stats = self.repository.get_user_stats(user_id)
        if not stats:
            raise NotFoundError(f"Gamification stats for user '{user_id}' not found.")

        stats.total_xp += max(0, xp_amount)
        self.db.flush()
        return stats.total_xp

    def get_all_achievements(self) -> List[AchievementResponse]:
        achievements = self.db.query(AchievementModel).all()
        return [AchievementResponse.model_validate(a) for a in achievements]

    def get_user_achievements(self, current_user: UserModel) -> List[UserAchievementResponse]:
        all_achievements = self.db.query(AchievementModel).all()
        user_earned = self.repository.get_user_achievements(current_user.id)
        earned_records = {ua.achievement_id: ua.earned_at for ua in user_earned}

        results: List[UserAchievementResponse] = []
        for ach in all_achievements:
            is_earned = ach.id in earned_records
            earned_at = earned_records.get(ach.id)
            results.append(
                UserAchievementResponse(
                    achievement=AchievementResponse.model_validate(ach),
                    is_earned=is_earned,
                    earned_at=earned_at,
                )
            )
        return results
