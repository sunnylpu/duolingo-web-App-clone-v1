"""
Modular Data-Driven Achievement Engine & Requirement Evaluator (Phase 27).
"""

from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from app.modules.gamification.models import (
    AchievementModel,
    UserAchievementModel,
    UserStatsModel,
)
from app.modules.progress.models import LessonAttemptModel, SkillProgressModel
from app.modules.lesson.models import SkillModel, LessonModel
from app.modules.course.models import UnitModel, CourseModel


class AchievementEngine:
    """Evaluates unearned achievements using data-driven requirement rules."""

    def __init__(self, db: Session):
        self.db = db

    def evaluate_user_achievements(
        self, user_id: str, course_id: Optional[str] = None
    ) -> List[AchievementModel]:
        """
        Evaluates unearned achievements for user_id.
        Returns list of newly unlocked AchievementModel objects.
        Anti-recursion rule: Bonus XP awards do NOT recursively invoke this method.
        """
        earned_ids = {
            ua.achievement_id
            for ua in self.db.query(UserAchievementModel.achievement_id)
            .filter(UserAchievementModel.user_id == user_id)
            .all()
        }

        unearned = (
            self.db.query(AchievementModel)
            .filter(AchievementModel.id.not_in(earned_ids) if earned_ids else True)
            .all()
        )

        if not unearned:
            return []

        stats = self.db.query(UserStatsModel).filter_by(user_id=user_id).first()
        total_xp = stats.total_xp if stats else 0
        streak = max(stats.current_streak if stats else 0, stats.longest_streak if stats else 0)

        completed_lesson_count = (
            self.db.query(LessonAttemptModel.lesson_id)
            .filter(LessonAttemptModel.user_id == user_id, LessonAttemptModel.status == "completed")
            .distinct()
            .count()
        )

        completed_skill_count = (
            self.db.query(SkillProgressModel)
            .filter(SkillProgressModel.user_id == user_id, SkillProgressModel.status == "completed")
            .count()
        )

        newly_unlocked: List[AchievementModel] = []
        total_bonus_xp = 0

        for ach in unearned:
            if ach.course_id and course_id and ach.course_id != course_id:
                continue

            current_val, is_met = self._evaluate_requirement(
                ach=ach,
                user_id=user_id,
                total_xp=total_xp,
                streak=streak,
                completed_lessons=completed_lesson_count,
                completed_skills=completed_skill_count,
            )

            if is_met:
                uach_id = f"uach_{user_id}_{ach.id}"
                new_ua = UserAchievementModel(
                    id=uach_id,
                    user_id=user_id,
                    achievement_id=ach.id,
                )
                self.db.add(new_ua)
                newly_unlocked.append(ach)
                total_bonus_xp += ach.xp_reward

        if total_bonus_xp > 0 and stats:
            stats.total_xp += total_bonus_xp
            stats.daily_xp += total_bonus_xp

        self.db.flush()
        return newly_unlocked

    def _evaluate_requirement(
        self,
        ach: AchievementModel,
        user_id: str,
        total_xp: int,
        streak: int,
        completed_lessons: int,
        completed_skills: int,
    ) -> Tuple[int, bool]:
        req_type = ach.requirement_type
        req_val = ach.requirement_value

        if req_type == "total_xp":
            return total_xp, total_xp >= req_val
        elif req_type == "streak":
            return streak, streak >= req_val
        elif req_type == "lessons_completed":
            return completed_lessons, completed_lessons >= req_val
        elif req_type == "skills_completed":
            return completed_skills, completed_skills >= req_val
        elif req_type == "units_completed":
            units = self.db.query(UnitModel).all()
            completed_units = 0
            for u in units:
                skill_count = len(u.skills)
                if skill_count > 0:
                    c_skills = (
                        self.db.query(SkillProgressModel)
                        .filter(
                            SkillProgressModel.user_id == user_id,
                            SkillProgressModel.skill_id.in_([s.id for s in u.skills]),
                            SkillProgressModel.status == "completed",
                        )
                        .count()
                    )
                    if c_skills == skill_count:
                        completed_units += 1
            return completed_units, completed_units >= req_val
        elif req_type == "course_completed":
            if not ach.course_id:
                return 0, False
            course = self.db.query(CourseModel).filter_by(id=ach.course_id).first()
            if not course:
                return 0, False
            c_units = len(course.units)
            completed_units = 0
            for u in course.units:
                skill_count = len(u.skills)
                if skill_count > 0:
                    c_skills = (
                        self.db.query(SkillProgressModel)
                        .filter(
                            SkillProgressModel.user_id == user_id,
                            SkillProgressModel.skill_id.in_([s.id for s in u.skills]),
                            SkillProgressModel.status == "completed",
                        )
                        .count()
                    )
                    if c_skills == skill_count:
                        completed_units += 1
            is_completed = (completed_units == c_units and c_units > 0)
            return completed_units, is_completed
        elif req_type == "course_skills_completed":
            if not ach.course_id:
                return 0, False
            c_skills = (
                self.db.query(SkillProgressModel)
                .join(SkillModel, SkillProgressModel.skill_id == SkillModel.id)
                .join(UnitModel, SkillModel.unit_id == UnitModel.id)
                .filter(
                    SkillProgressModel.user_id == user_id,
                    UnitModel.course_id == ach.course_id,
                    SkillProgressModel.status == "completed",
                )
                .count()
            )
            return c_skills, c_skills >= req_val
        elif req_type == "reviews_completed":
            return completed_lessons, completed_lessons >= req_val

        return 0, False

    def get_achievement_progress_for_user(
        self, user_id: str, category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        query = self.db.query(AchievementModel)
        if category and category.lower() != "all":
            query = query.filter(AchievementModel.category == category.lower())

        achievements = query.all()

        user_ach_map = {
            ua.achievement_id: ua
            for ua in self.db.query(UserAchievementModel)
            .filter(UserAchievementModel.user_id == user_id)
            .all()
        }

        stats = self.db.query(UserStatsModel).filter_by(user_id=user_id).first()
        total_xp = stats.total_xp if stats else 0
        streak = max(stats.current_streak if stats else 0, stats.longest_streak if stats else 0)

        completed_lessons = (
            self.db.query(LessonAttemptModel.lesson_id)
            .filter(LessonAttemptModel.user_id == user_id, LessonAttemptModel.status == "completed")
            .distinct()
            .count()
        )

        completed_skills = (
            self.db.query(SkillProgressModel)
            .filter(SkillProgressModel.user_id == user_id, SkillProgressModel.status == "completed")
            .count()
        )

        results: List[Dict[str, Any]] = []

        for ach in achievements:
            earned_record = user_ach_map.get(ach.id)
            is_earned = earned_record is not None

            current_val, _ = self._evaluate_requirement(
                ach=ach,
                user_id=user_id,
                total_xp=total_xp,
                streak=streak,
                completed_lessons=completed_lessons,
                completed_skills=completed_skills,
            )

            results.append(
                {
                    "id": ach.id,
                    "code": ach.code,
                    "name": ach.name,
                    "description": ach.description,
                    "icon": ach.icon,
                    "category": ach.category,
                    "rarity": ach.rarity,
                    "xp_reward": ach.xp_reward,
                    "requirement_type": ach.requirement_type,
                    "requirement_value": ach.requirement_value,
                    "course_id": ach.course_id,
                    "earned": is_earned,
                    "earned_at": earned_record.earned_at if earned_record else None,
                    "current_value": current_val if not is_earned else ach.requirement_value,
                    "target_value": ach.requirement_value,
                }
            )

        return results
