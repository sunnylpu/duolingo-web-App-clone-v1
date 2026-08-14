import uuid
from datetime import datetime, date, timedelta, timezone
from typing import List, Dict, Any, Optional, Union
from sqlalchemy.orm import Session
from app.config import settings
from app.shared.clock import Clock, system_clock
from app.modules.gamification.repository import GamificationRepository
from app.modules.progress.repository import ProgressRepository
from app.modules.progress.models import DailyActivityModel, LessonAttemptModel
from app.modules.gamification.models import AchievementModel, UserAchievementModel, UserStatsModel
from app.modules.gamification.achievements.engine import AchievementEngine
from app.modules.lesson.models import ExerciseModel
from app.modules.user.models import UserModel
from app.modules.gamification.schemas import (
    GamificationStatsResponse,
    DailyActivityResponse,
    AchievementResponse,
    UserAchievementResponse,
    HeartRegenerationInfo,
    PracticeExerciseResponse,
    PracticeSubmissionResponse,
    HeartRefillResponse,
)
from app.shared.errors import NotFoundError, ValidationError, ConflictError
import zoneinfo


def get_current_activity_date() -> date:
    """Returns today's date according to the configured APP_TIMEZONE setting."""
    try:
        tz = zoneinfo.ZoneInfo(settings.APP_TIMEZONE)
        return datetime.now(tz).date()
    except Exception:
        return datetime.utcnow().date()


class GamificationService:
    """Contains business logic for Gamification metrics, Streaks, Daily Goals, Achievements, and Heart Regeneration."""

    def __init__(self, db: Session, clock: Optional[Clock] = None):
        self.db = db
        self.clock = clock or system_clock
        self.repository = GamificationRepository(db)
        self.progress_repository = ProgressRepository(db)
        self.achievement_engine = AchievementEngine(db)

    def refresh_hearts(self, user_id: str) -> UserStatsModel:
        stats = self.repository.get_user_stats(user_id)
        if not stats:
            raise NotFoundError(f"Gamification stats for user '{user_id}' not found.")

        current_time = self.clock.now()
        if current_time.tzinfo is None:
            current_time = current_time.replace(tzinfo=timezone.utc)

        max_hearts = settings.MAX_HEARTS
        interval_seconds = settings.HEART_REGEN_MINUTES * 60

        if stats.hearts >= max_hearts:
            stats.hearts = max_hearts
            stats.last_heart_regeneration_at = None
            self.db.flush()
            return stats

        last_regen = stats.last_heart_regeneration_at
        if last_regen is None:
            stats.last_heart_regeneration_at = current_time
            self.db.flush()
            return stats

        if last_regen.tzinfo is None:
            last_regen = last_regen.replace(tzinfo=timezone.utc)

        elapsed = (current_time - last_regen).total_seconds()
        if elapsed >= interval_seconds:
            intervals_gained = int(elapsed // interval_seconds)
            new_hearts = min(max_hearts, stats.hearts + intervals_gained)

            if new_hearts >= max_hearts:
                stats.hearts = max_hearts
                stats.last_heart_regeneration_at = None
            else:
                stats.hearts = new_hearts
                stats.last_heart_regeneration_at = last_regen + timedelta(seconds=intervals_gained * interval_seconds)

            self.db.flush()

        return stats

    def get_heart_regeneration_info(self, stats: UserStatsModel) -> HeartRegenerationInfo:
        max_hearts = settings.MAX_HEARTS
        interval_seconds = settings.HEART_REGEN_MINUTES * 60

        if stats.hearts >= max_hearts or not stats.last_heart_regeneration_at:
            return HeartRegenerationInfo(
                enabled=True,
                seconds_until_next=None,
                interval_seconds=interval_seconds,
            )

        current_time = self.clock.now()
        if current_time.tzinfo is None:
            current_time = current_time.replace(tzinfo=timezone.utc)

        last_regen = stats.last_heart_regeneration_at
        if last_regen.tzinfo is None:
            last_regen = last_regen.replace(tzinfo=timezone.utc)

        elapsed = (current_time - last_regen).total_seconds()
        remaining = max(0, int(interval_seconds - (elapsed % interval_seconds)))

        return HeartRegenerationInfo(
            enabled=True,
            seconds_until_next=remaining,
            interval_seconds=interval_seconds,
        )

    def get_user_stats(self, current_user: UserModel) -> GamificationStatsResponse:
        stats = self.refresh_hearts(current_user.id)

        today_date = current_user.stats.last_active_date or date.today()
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
        regen_info = self.get_heart_regeneration_info(stats)

        return GamificationStatsResponse(
            total_xp=stats.total_xp,
            current_streak=stats.current_streak,
            longest_streak=stats.longest_streak,
            hearts=stats.hearts,
            max_hearts=settings.MAX_HEARTS,
            heart_regeneration=regen_info,
            gems=stats.gems,
            daily_goal_xp=stats.daily_goal_xp,
            daily_xp=daily_xp,
            daily_goal_completed=goal_completed,
            activity_date=today_date.isoformat(),
        )

    def deduct_heart(self, user_id: str) -> int:
        stats = self.refresh_hearts(user_id)
        if stats.hearts <= 0:
            stats.hearts = 0
            self.db.flush()
            return 0

        stats.hearts = max(stats.hearts - 1, 0)
        if stats.last_heart_regeneration_at is None:
            curr = self.clock.now()
            if curr.tzinfo is None:
                curr = curr.replace(tzinfo=timezone.utc)
            stats.last_heart_regeneration_at = curr

        self.db.flush()
        return stats.hearts

    def get_practice_exercise(self) -> PracticeExerciseResponse:
        exercise = self.db.query(ExerciseModel).first()
        if exercise:
            return PracticeExerciseResponse(
                exercise_id=exercise.id,
                prompt=exercise.prompt,
                type=exercise.type,
                correct_answer=exercise.correct_answer,
                data=exercise.data,
            )

        return PracticeExerciseResponse(
            exercise_id="ex_practice_default",
            prompt="Translate to Spanish: 'Hello'",
            type="multiple_choice",
            correct_answer="Hola",
            data={"options": ["Hola", "Adiós", "Gracias", "Por favor"]},
        )

    def submit_practice_answer(
        self, user_id: str, exercise_id: str, answer: Union[str, Dict[str, Any], List[Any]]
    ) -> PracticeSubmissionResponse:
        stats = self.refresh_hearts(user_id)

        if stats.hearts >= settings.MAX_HEARTS:
            raise ValidationError("You already have full hearts.", code="HEARTS_FULL")

        current_time = self.clock.now()
        if current_time.tzinfo is None:
            current_time = current_time.replace(tzinfo=timezone.utc)

        if stats.last_practice_recovery_at:
            last_pract = stats.last_practice_recovery_at
            if last_pract.tzinfo is None:
                last_pract = last_pract.replace(tzinfo=timezone.utc)
            cooldown_seconds = settings.PRACTICE_RECOVERY_COOLDOWN_MINUTES * 60
            if (current_time - last_pract).total_seconds() < cooldown_seconds:
                raise ValidationError(
                    "Practice recovery is temporarily unavailable.", code="PRACTICE_COOLDOWN"
                )

        exercise = self.db.query(ExerciseModel).filter(ExerciseModel.id == exercise_id).first()
        correct_ans = exercise.correct_answer if exercise else "Hola"

        ans_str = str(answer).strip().lower()
        target_str = str(correct_ans).strip().lower()
        is_correct = (ans_str == target_str)

        if is_correct:
            stats.hearts = min(settings.MAX_HEARTS, stats.hearts + 1)
            stats.last_practice_recovery_at = current_time
            if stats.hearts >= settings.MAX_HEARTS:
                stats.last_heart_regeneration_at = None
            self.db.commit()

        return PracticeSubmissionResponse(
            is_correct=is_correct,
            correct_answer=correct_ans,
            hearts=stats.hearts,
            max_hearts=settings.MAX_HEARTS,
            recovered=1 if is_correct else 0,
        )

    def refill_hearts(self, user_id: str) -> HeartRefillResponse:
        stats = self.repository.get_user_stats(user_id)
        if not stats:
            raise NotFoundError(f"Gamification stats for user '{user_id}' not found.")

        stats.hearts = settings.MAX_HEARTS
        stats.last_heart_regeneration_at = None
        self.db.commit()

        return HeartRefillResponse(
            hearts=settings.MAX_HEARTS,
            max_hearts=settings.MAX_HEARTS,
            refilled=True,
        )

    def award_lesson_xp(self, user_id: str, xp_amount: int) -> int:
        stats = self.repository.get_user_stats(user_id)
        if not stats:
            raise NotFoundError(f"Gamification stats for user '{user_id}' not found.")
        stats.total_xp += max(0, xp_amount)
        self.db.flush()
        return stats.total_xp

    def update_streak_and_daily_goal(
        self, user_id: str, xp_earned: int, activity_date_override: Optional[date] = None
    ) -> Dict[str, Any]:
        stats = self.repository.get_user_stats(user_id)
        if not stats:
            raise NotFoundError(f"Gamification stats for user '{user_id}' not found.")

        current_date = activity_date_override or date.today()
        last_active = stats.last_active_date
        streak_increased = False

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

    def evaluate_achievements(
        self, user_id: str, course_id: Optional[str] = None, commit: bool = True
    ) -> List[AchievementResponse]:
        newly_earned_models = self.achievement_engine.evaluate_user_achievements(
            user_id=user_id, course_id=course_id
        )
        if commit:
            self.db.commit()
        else:
            self.db.flush()

        return [AchievementResponse.model_validate(ach) for ach in newly_earned_models]

    def get_all_achievements(self, category: Optional[str] = None) -> List[AchievementResponse]:
        query = self.db.query(AchievementModel)
        if category and category.lower() != "all":
            query = query.filter(AchievementModel.category == category.lower())
        achievements = query.all()
        return [AchievementResponse.model_validate(a) for a in achievements]

    def get_user_achievements(
        self, current_user: UserModel, category: Optional[str] = None
    ) -> List[UserAchievementResponse]:
        progress_data = self.achievement_engine.get_achievement_progress_for_user(
            user_id=current_user.id, category=category
        )

        results: List[UserAchievementResponse] = []
        for item in progress_data:
            ach_resp = AchievementResponse(
                id=item["id"],
                code=item["code"],
                name=item["name"],
                description=item["description"],
                icon=item["icon"],
                category=item["category"],
                rarity=item["rarity"],
                xp_reward=item["xp_reward"],
                requirement_type=item["requirement_type"],
                requirement_value=item["requirement_value"],
                course_id=item["course_id"],
            )
            results.append(
                UserAchievementResponse(
                    achievement=ach_resp,
                    is_earned=item["earned"],
                    earned_at=item["earned_at"],
                    progress=item["current_value"],
                    target=item["target_value"],
                )
            )

        return results
