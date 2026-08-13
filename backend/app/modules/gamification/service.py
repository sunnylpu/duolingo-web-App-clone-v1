import uuid
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional
import zoneinfo
from sqlalchemy.orm import Session
from app.config import settings
from app.modules.gamification.repository import GamificationRepository
from app.modules.progress.repository import ProgressRepository
from app.modules.progress.models import DailyActivityModel, LessonAttemptModel, SkillProgressModel
from app.modules.gamification.models import AchievementModel, UserAchievementModel
from app.modules.user.models import UserModel
from app.modules.gamification.schemas import (
    GamificationStatsResponse,
    DailyActivityResponse,
    AchievementResponse,
    UserAchievementResponse,
)
from app.shared.errors import NotFoundError


def get_current_activity_date() -> date:
    """Returns today's date according to the configured APP_TIMEZONE setting."""
    try:
        tz = zoneinfo.ZoneInfo(settings.APP_TIMEZONE)
        return datetime.now(tz).date()
    except Exception:
        return datetime.utcnow().date()


class GamificationService:
    """Contains business logic for Gamification metrics, Streaks, Daily Goals, and Achievements."""

    def __init__(self, db: Session):
        self.db = db
        self.repository = GamificationRepository(db)
        self.progress_repository = ProgressRepository(db)

    def get_user_stats(self, current_user: UserModel) -> GamificationStatsResponse:
        stats = self.repository.get_user_stats(current_user.id)
        if not stats and current_user.stats:
            stats = current_user.stats

        if not stats:
            raise NotFoundError("Gamification statistics not found.")

        today_date = get_current_activity_date()
        today_act = (
            self.db.query(DailyActivityModel)
            .filter(
                DailyActivityModel.user_id == current_user.id,
                DailyActivityModel.activity_date == today_date,
            )
            .first()
        )

        daily_xp = today_act.xp_earned if today_act else 0
        goal_completed = today_act.goal_completed if today_act else (daily_xp >= stats.daily_goal_xp)

        return GamificationStatsResponse(
            total_xp=stats.total_xp,
            current_streak=stats.current_streak,
            longest_streak=stats.longest_streak,
            hearts=stats.hearts,
            gems=stats.gems,
            daily_goal_xp=stats.daily_goal_xp,
            daily_xp=daily_xp,
            daily_goal_completed=goal_completed,
            activity_date=today_date.isoformat(),
        )

    def get_today_activity(self, current_user: UserModel) -> DailyActivityResponse:
        stats = self.repository.get_user_stats(current_user.id)
        goal_xp = stats.daily_goal_xp if stats else 30

        today_date = get_current_activity_date()
        today_act = (
            self.db.query(DailyActivityModel)
            .filter(
                DailyActivityModel.user_id == current_user.id,
                DailyActivityModel.activity_date == today_date,
            )
            .first()
        )

        if not today_act:
            return DailyActivityResponse(
                date=today_date.isoformat(),
                xp_earned=0,
                lessons_completed=0,
                goal_xp=goal_xp,
                goal_completed=False,
            )

        return DailyActivityResponse(
            date=today_act.activity_date.isoformat(),
            xp_earned=today_act.xp_earned,
            lessons_completed=today_act.lessons_completed,
            goal_xp=goal_xp,
            goal_completed=today_act.goal_completed,
        )

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

    def update_streak_and_daily_goal(
        self, user_id: str, xp_earned: int, activity_date_override: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        Calculates and updates user's current streak, longest streak, and daily goal completion.
        Executed inside the lesson completion database transaction.
        """
        stats = self.repository.get_user_stats(user_id)
        if not stats:
            raise NotFoundError(f"Gamification stats for user '{user_id}' not found.")

        current_date = activity_date_override or get_current_activity_date()
        last_active = stats.last_active_date

        streak_increased = False

        # Deterministic Streak Algorithm
        if last_active is None:
            stats.current_streak = 1
            streak_increased = True
        elif last_active == current_date:
            streak_increased = False
        elif last_active == current_date - timedelta(days=1):
            stats.current_streak += 1
            streak_increased = True
        else:
            stats.current_streak = 1
            streak_increased = True

        stats.longest_streak = max(stats.longest_streak, stats.current_streak)
        stats.last_active_date = current_date

        today_act = (
            self.db.query(DailyActivityModel)
            .filter(
                DailyActivityModel.user_id == user_id,
                DailyActivityModel.activity_date == current_date,
            )
            .first()
        )

        was_goal_completed = today_act.goal_completed if today_act else False
        current_daily_xp = (today_act.xp_earned if today_act else 0)

        stats.daily_xp = current_daily_xp
        is_goal_now_completed = current_daily_xp >= stats.daily_goal_xp
        goal_just_completed = (not was_goal_completed) and is_goal_now_completed

        if today_act:
            today_act.goal_completed = is_goal_now_completed

        self.db.flush()

        return {
            "streak": {
                "current": stats.current_streak,
                "longest": stats.longest_streak,
                "increased": streak_increased,
            },
            "daily_progress": {
                "xp": current_daily_xp,
                "goal": stats.daily_goal_xp,
                "goal_completed": is_goal_now_completed,
                "goal_just_completed": goal_just_completed,
            },
        }

    def evaluate_achievements(self, user_id: str, commit: bool = True) -> List[AchievementResponse]:
        """
        Data-driven achievement evaluation. Checks user state against achievement requirements
        and idempotently grants newly unlocked achievements.
        """
        all_achievements = self.db.query(AchievementModel).all()
        user_earned = self.repository.get_user_achievements(user_id)
        earned_ids = {ua.achievement_id for ua in user_earned}

        stats = self.repository.get_user_stats(user_id)
        total_xp = stats.total_xp if stats else 0
        current_streak = stats.current_streak if stats else 0

        # Unique completed lessons count
        completed_attempts = (
            self.db.query(LessonAttemptModel)
            .filter(
                LessonAttemptModel.user_id == user_id,
                LessonAttemptModel.status == "completed",
            )
            .all()
        )
        unique_completed_lessons = {a.lesson_id for a in completed_attempts}
        lessons_completed_count = len(unique_completed_lessons)

        newly_earned: List[AchievementResponse] = []

        for ach in all_achievements:
            if ach.id in earned_ids:
                continue

            satisfied = False
            req_type = ach.requirement_type
            req_val = ach.requirement_value

            if req_type == "lessons_completed":
                satisfied = lessons_completed_count >= req_val
            elif req_type == "total_xp":
                satisfied = total_xp >= req_val
            elif req_type == "streak":
                satisfied = current_streak >= req_val

            if satisfied:
                ua_id = f"uach_{user_id}_{ach.id}"
                self.repository.grant_user_achievement(
                    user_achievement_id=ua_id,
                    user_id=user_id,
                    achievement_id=ach.id,
                )
                newly_earned.append(AchievementResponse.model_validate(ach))

        if commit:
            self.db.commit()
        else:
            self.db.flush()

        return newly_earned

    def get_all_achievements(self) -> List[AchievementResponse]:
        achievements = self.db.query(AchievementModel).all()
        return [AchievementResponse.model_validate(a) for a in achievements]

    def get_user_achievements(self, current_user: UserModel) -> List[UserAchievementResponse]:
        all_achievements = self.db.query(AchievementModel).all()
        user_earned = self.repository.get_user_achievements(current_user.id)
        earned_records = {ua.achievement_id: ua.earned_at for ua in user_earned}

        stats = self.repository.get_user_stats(current_user.id)
        total_xp = stats.total_xp if stats else 0
        current_streak = stats.current_streak if stats else 0

        completed_attempts = (
            self.db.query(LessonAttemptModel)
            .filter(
                LessonAttemptModel.user_id == current_user.id,
                LessonAttemptModel.status == "completed",
            )
            .all()
        )
        lessons_completed_count = len({a.lesson_id for a in completed_attempts})

        results: List[UserAchievementResponse] = []
        for ach in all_achievements:
            is_earned = ach.id in earned_records
            earned_at = earned_records.get(ach.id)

            # Determine progress for locked achievements
            curr_val = 0
            if ach.requirement_type == "lessons_completed":
                curr_val = lessons_completed_count
            elif ach.requirement_type == "total_xp":
                curr_val = total_xp
            elif ach.requirement_type == "streak":
                curr_val = current_streak

            progress_val = ach.requirement_value if is_earned else min(curr_val, ach.requirement_value)

            results.append(
                UserAchievementResponse(
                    achievement=AchievementResponse.model_validate(ach),
                    is_earned=is_earned,
                    earned_at=earned_at,
                    progress=progress_val,
                    target=ach.requirement_value,
                )
            )
        return results
