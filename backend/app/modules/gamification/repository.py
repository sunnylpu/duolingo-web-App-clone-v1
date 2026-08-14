from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.gamification.models import (
    UserStatsModel,
    AchievementModel,
    UserAchievementModel,
)


class GamificationRepository:
    """Handles data persistence for UserStats and Achievements."""

    def __init__(self, db: Session):
        self.db = db

    def get_user_stats(self, user_id: str) -> Optional[UserStatsModel]:
        return self.db.query(UserStatsModel).filter(UserStatsModel.user_id == user_id).first()

    def create_or_update_user_stats(
        self,
        stats_id: str,
        user_id: str,
        total_xp: int = 0,
        current_streak: int = 0,
        longest_streak: int = 0,
        hearts: int = 5,
        gems: int = 500,
        daily_goal_xp: int = 20,
        daily_xp: int = 0,
    ) -> UserStatsModel:
        stats = self.get_user_stats(user_id)
        if not stats:
            stats = UserStatsModel(
                id=stats_id,
                user_id=user_id,
                total_xp=total_xp,
                current_streak=current_streak,
                longest_streak=longest_streak,
                hearts=hearts,
                gems=gems,
                daily_goal_xp=daily_goal_xp,
                daily_xp=daily_xp,
            )
            self.db.add(stats)
        else:
            stats.total_xp = total_xp
            stats.current_streak = current_streak
            stats.longest_streak = longest_streak
            stats.hearts = hearts
            stats.gems = gems
            stats.daily_goal_xp = daily_goal_xp
            stats.daily_xp = daily_xp

        self.db.commit()
        self.db.refresh(stats)
        return stats

    def get_achievement_by_code(self, code: str) -> Optional[AchievementModel]:
        return self.db.query(AchievementModel).filter(AchievementModel.code == code).first()

    def create_achievement(
        self,
        achievement_id: str,
        code: str,
        name: str,
        description: str,
        icon: str,
        requirement_type: str,
        requirement_value: int,
        category: str = "learning",
        course_id: Optional[str] = None,
        rarity: str = "common",
        xp_reward: int = 0,
    ) -> AchievementModel:
        achievement = self.get_achievement_by_code(code)
        if not achievement:
            achievement = AchievementModel(
                id=achievement_id,
                code=code,
                name=name,
                description=description,
                icon=icon,
                category=category,
                requirement_type=requirement_type,
                requirement_value=requirement_value,
                course_id=course_id,
                rarity=rarity,
                xp_reward=xp_reward,
            )
            self.db.add(achievement)
            self.db.commit()
            self.db.refresh(achievement)
        else:
            achievement.category = category
            achievement.course_id = course_id
            achievement.rarity = rarity
            achievement.xp_reward = xp_reward
            self.db.commit()
        return achievement

    def grant_user_achievement(
        self,
        user_achievement_id: str,
        user_id: str,
        achievement_id: str,
    ) -> UserAchievementModel:
        record = (
            self.db.query(UserAchievementModel)
            .filter(
                UserAchievementModel.user_id == user_id,
                UserAchievementModel.achievement_id == achievement_id,
            )
            .first()
        )
        if not record:
            record = UserAchievementModel(
                id=user_achievement_id,
                user_id=user_id,
                achievement_id=achievement_id,
            )
            self.db.add(record)
            self.db.commit()
            self.db.refresh(record)
        return record

    def get_user_achievements(self, user_id: str) -> List[UserAchievementModel]:
        return self.db.query(UserAchievementModel).filter(UserAchievementModel.user_id == user_id).all()
