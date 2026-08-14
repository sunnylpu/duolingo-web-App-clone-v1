import re
import uuid
import json
from datetime import datetime, date
from typing import List, Optional, Any
from sqlalchemy.orm import Session, joinedload
from app.modules.lesson.repository import LessonRepository
from app.modules.gamification.service import GamificationService
from app.modules.progress.repository import ProgressRepository
from app.modules.lesson.validators import validator_registry
from app.modules.lesson.models import LessonModel, SkillModel
from app.modules.course.models import UnitModel
from app.modules.progress.models import LessonAttemptModel
from app.modules.lesson.schemas import (
    LessonDetailResponse,
    LessonStartResponse,
    AnswerSubmissionResponse,
    LessonCompleteResponse,
)
from app.modules.user.models import UserModel
from app.shared.errors import NotFoundError, ValidationError, ConflictError


class LessonService:
    """Contains business logic for Skills, Lessons, Exercises, and Lesson Sessions."""

    def __init__(self, db: Session):
        self.db = db
        self.repository = LessonRepository(db)
        self.gamification_service = GamificationService(db)
        self.progress_repository = ProgressRepository(db)

    def get_lesson_detail(self, lesson_id: str) -> LessonDetailResponse:
        lesson = self.repository.get_lesson_by_id(lesson_id)
        if not lesson:
            raise NotFoundError(f"Lesson with ID '{lesson_id}' was not found.")
        return LessonDetailResponse.model_validate(lesson)

    def start_lesson(
        self, current_user: UserModel, lesson_id: str
    ) -> LessonStartResponse:
        self.gamification_service.refresh_hearts(current_user.id)
        lesson = self.repository.get_lesson_by_id(lesson_id)
        if not lesson:
            raise NotFoundError(f"Lesson with ID '{lesson_id}' was not found.")

        # Business Access Control: Validate progression status for skill
        from app.modules.progress.service import ProgressService
        progress_service = ProgressService(self.db)
        skill_state = progress_service.get_skill_status(current_user.id, lesson.skill_id)

        if skill_state.get("status") == "locked":
            raise ConflictError("Complete the prerequisite skill first.", code="SKILL_LOCKED")

        existing_attempt = self.repository.get_active_lesson_attempt(
            user_id=current_user.id, lesson_id=lesson_id
        )
        if existing_attempt:
            return LessonStartResponse(
                attempt_id=existing_attempt.id,
                lesson_id=existing_attempt.lesson_id,
                status=existing_attempt.status,
                started_at=existing_attempt.started_at,
            )

        try:
            attempt = self.repository.create_lesson_attempt(
                user_id=current_user.id, lesson_id=lesson_id
            )
            self.db.commit()
            self.db.refresh(attempt)
            return LessonStartResponse(
                attempt_id=attempt.id,
                lesson_id=attempt.lesson_id,
                status=attempt.status,
                started_at=attempt.started_at,
            )
        except Exception:
            self.db.rollback()
            raise

    def submit_exercise_answer(
        self,
        current_user: UserModel,
        lesson_id: str,
        exercise_id: str,
        attempt_id: str,
        user_answer: Any,
    ) -> AnswerSubmissionResponse:
        lesson = self.repository.get_lesson_by_id(lesson_id)
        if not lesson:
            raise NotFoundError(f"Lesson with ID '{lesson_id}' was not found.")

        exercise = self.repository.get_exercise_by_id(exercise_id)
        if not exercise:
            raise NotFoundError(f"Exercise with ID '{exercise_id}' was not found.")
        if exercise.lesson_id != lesson_id:
            raise ValidationError(
                f"Exercise '{exercise_id}' does not belong to lesson '{lesson_id}'."
            )

        attempt = self.repository.get_lesson_attempt_by_id(attempt_id)
        if not attempt:
            raise NotFoundError(f"Lesson attempt '{attempt_id}' was not found.")

        if attempt.user_id != current_user.id:
            raise ValidationError("Lesson attempt belongs to another user.")

        if attempt.lesson_id != lesson_id:
            raise ValidationError(
                f"Lesson attempt '{attempt_id}' is not for lesson '{lesson_id}'."
            )
        if attempt.status != "started":
            raise ValidationError("LESSON_ATTEMPT_NOT_ACTIVE")

        existing_ex_attempt = self.repository.get_exercise_attempt(
            lesson_attempt_id=attempt_id, exercise_id=exercise_id
        )
        if existing_ex_attempt:
            user_stats = current_user.stats
            hearts_rem = user_stats.hearts if user_stats else 5
            return AnswerSubmissionResponse(
                exercise_id=exercise_id,
                is_correct=existing_ex_attempt.is_correct,
                correct_answer=exercise.correct_answer,
                hearts_lost=0,
                hearts_remaining=hearts_rem,
                attempt_completed=False,
            )

        refreshed_stats = self.gamification_service.refresh_hearts(current_user.id)
        current_hearts = refreshed_stats.hearts
        if current_hearts <= 0:
            raise ConflictError("You have no hearts remaining.", code="OUT_OF_HEARTS")

        validator = validator_registry.get_validator(exercise.type)
        val_result = validator.validate(exercise=exercise, submitted_answer=user_answer)
        is_correct = val_result.is_correct

        stored_answer_str = (
            json.dumps(user_answer) if isinstance(user_answer, (dict, list)) else str(user_answer)
        )

        try:
            hearts_lost = 0
            hearts_remaining = current_hearts

            if not is_correct:
                hearts_lost = 1
                hearts_remaining = self.gamification_service.deduct_heart(current_user.id)

            self.repository.create_exercise_attempt(
                lesson_attempt_id=attempt_id,
                exercise_id=exercise_id,
                answer=stored_answer_str,
                is_correct=is_correct,
                hearts_lost=hearts_lost,
            )

            self.db.commit()

            return AnswerSubmissionResponse(
                exercise_id=exercise_id,
                is_correct=is_correct,
                correct_answer=val_result.correct_answer,
                hearts_lost=hearts_lost,
                hearts_remaining=hearts_remaining,
                attempt_completed=False,
            )
        except Exception:
            self.db.rollback()
            raise

    def complete_lesson(
        self,
        current_user: UserModel,
        lesson_id: str,
        attempt_id: str,
    ) -> LessonCompleteResponse:
        lesson = self.repository.get_lesson_by_id(lesson_id)
        if not lesson:
            raise NotFoundError(f"Lesson with ID '{lesson_id}' was not found.")

        attempt = self.repository.get_lesson_attempt_by_id(attempt_id)
        if not attempt:
            raise NotFoundError(f"Lesson attempt '{attempt_id}' was not found.")

        if attempt.user_id != current_user.id:
            raise ValidationError("Lesson attempt belongs to another user.")
        if attempt.lesson_id != lesson_id:
            raise ValidationError(
                f"Lesson attempt '{attempt_id}' is not for lesson '{lesson_id}'."
            )

        def get_skill_progress_data(skill_id: str) -> dict:
            sp = self.progress_repository.get_skill_progress(current_user.id, skill_id)
            if sp:
                return {
                    "completion_percent": sp.completion_percent,
                    "crown_level": sp.crown_level,
                    "status": sp.status,
                    "lessons_completed": sp.lessons_completed,
                }
            return {
                "completion_percent": 100.0,
                "crown_level": 1,
                "status": "completed",
                "lessons_completed": 1,
            }

        # Idempotency check for repeated requests
        if attempt.status == "completed":
            sp_data = get_skill_progress_data(lesson.skill_id)
            return LessonCompleteResponse(
                lesson_id=lesson_id,
                attempt_id=attempt_id,
                status="completed",
                xp_earned=0,
                unit_bonus_xp=0,
                unit_completed=False,
                unit=None,
                score=attempt.score,
                skill_progress=sp_data,
                already_completed=True,
            )

        if attempt.status != "started":
            raise ValidationError("LESSON_ATTEMPT_NOT_ACTIVE")

        lesson_exercises = self.repository.get_exercises_by_lesson(lesson_id)
        answered_exercise_ids = {ex.exercise_id for ex in attempt.exercise_attempts}

        if len(answered_exercise_ids) < len(lesson_exercises):
            raise ValidationError(
                "Not all exercises have been answered.", details={"code": "LESSON_NOT_COMPLETE"}
            )

        try:
            total_count = len(lesson_exercises)
            correct_count = sum(1 for ex in attempt.exercise_attempts if ex.is_correct)
            score = int(round((correct_count / total_count) * 100)) if total_count > 0 else 100

            attempt.status = "completed"
            attempt.completed_at = datetime.utcnow()
            attempt.score = score
            attempt.xp_earned = lesson.xp_reward

            self.gamification_service.award_lesson_xp(current_user.id, lesson.xp_reward)

            from app.modules.gamification.service import get_current_activity_date
            today_date = get_current_activity_date()

            act_id = f"act_{uuid.uuid4().hex[:12]}"
            self.progress_repository.record_daily_activity(
                activity_id=act_id,
                user_id=current_user.id,
                activity_date=today_date,
                xp_earned=lesson.xp_reward,
                lessons_completed=1,
                commit=False,
            )

            streak_daily_info = self.gamification_service.update_streak_and_daily_goal(
                user_id=current_user.id,
                xp_earned=lesson.xp_reward,
                activity_date_override=today_date,
            )

            # Update Skill Progress
            skill_id = lesson.skill_id
            skill_lessons = self.repository.get_lessons_by_skill(skill_id)
            skill_lesson_ids = {l.id for l in skill_lessons}

            completed_attempts = (
                self.db.query(LessonAttemptModel)
                .filter(
                    LessonAttemptModel.user_id == current_user.id,
                    LessonAttemptModel.lesson_id.in_(skill_lesson_ids),
                    LessonAttemptModel.status == "completed",
                )
                .all()
            )
            unique_completed_lessons = {a.lesson_id for a in completed_attempts}
            unique_completed_lessons.add(lesson_id)

            completed_count = len(unique_completed_lessons)
            total_skill_lessons = max(1, len(skill_lessons))
            completion_percent = float(min(100.0, (completed_count / total_skill_lessons) * 100.0))
            crown_level = min(5, completed_count)
            skill_status = "completed" if completion_percent >= 100.0 else "in_progress"

            sp_id = f"sp_{uuid.uuid4().hex[:12]}"
            self.progress_repository.upsert_skill_progress(
                progress_id=sp_id,
                user_id=current_user.id,
                skill_id=skill_id,
                status=skill_status,
                completion_percent=completion_percent,
                crown_level=crown_level,
                lessons_completed=completed_count,
                xp_earned=completed_count * lesson.xp_reward,
                commit=False,
            )

            # ── Unit completion evaluation & milestone check ─────────────
            unit_bonus_xp = 0
            unit_completed = False
            unit_data = None

            target_skill = (
                self.db.query(SkillModel)
                .options(joinedload(SkillModel.unit))
                .filter(SkillModel.id == skill_id)
                .first()
            )
            if target_skill and target_skill.unit:
                unit = target_skill.unit
                unit_skills = (
                    self.db.query(SkillModel)
                    .filter(SkillModel.unit_id == unit.id)
                    .all()
                )
                from app.modules.progress.service import ProgressService
                progress_service = ProgressService(self.db)
                completed_lesson_ids = progress_service._fetch_completed_lesson_ids(current_user.id)
                completed_lesson_ids.add(lesson_id)
                user_progress_map = progress_service._fetch_user_skill_progress_map(current_user.id)

                all_unit_skills_completed = True
                cache: Dict[str, str] = {}
                skill_map = {s.id: s for s in unit_skills}

                for u_skill in unit_skills:
                    state = progress_service._evaluate_skill_state_from_memory(
                        u_skill, completed_lesson_ids, cache, skill_map, user_progress_map
                    )
                    if state["status"] != "completed":
                        all_unit_skills_completed = False
                        break

                if all_unit_skills_completed:
                    milestone_info = progress_service.check_and_grant_unit_milestone(
                        user_id=current_user.id, unit_id=unit.id
                    )
                    unit_bonus_xp = milestone_info["unit_bonus_xp"]
                    unit_completed = milestone_info["unit_completed"]
                    unit_data = {
                        "id": unit.id,
                        "title": unit.title,
                        "status": "completed",
                        "completion_percent": 100.0,
                    }

            # Evaluate achievements
            newly_earned_achs = self.gamification_service.evaluate_achievements(
                user_id=current_user.id, commit=False
            )
            newly_earned_data = [
                {
                    "code": a.code,
                    "name": a.name,
                    "description": a.description,
                    "icon": a.icon,
                }
                for a in newly_earned_achs
            ]

            self.db.commit()

            sp_data = {
                "completion_percent": completion_percent,
                "crown_level": crown_level,
                "status": skill_status,
                "lessons_completed": completed_count,
            }

            return LessonCompleteResponse(
                lesson_id=lesson_id,
                attempt_id=attempt_id,
                status="completed",
                xp_earned=lesson.xp_reward,
                unit_bonus_xp=unit_bonus_xp,
                unit_completed=unit_completed,
                unit=unit_data,
                score=score,
                skill_progress=sp_data,
                streak=streak_daily_info.get("streak"),
                daily_progress=streak_daily_info.get("daily_progress"),
                achievements={"newly_earned": newly_earned_data},
                already_completed=False,
            )
        except Exception:
            self.db.rollback()
            raise
