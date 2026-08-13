import re
from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.lesson.repository import LessonRepository
from app.modules.gamification.service import GamificationService
from app.modules.lesson.schemas import (
    LessonDetailResponse,
    LessonStartResponse,
    AnswerSubmissionResponse,
)
from app.modules.user.models import UserModel
from app.shared.errors import NotFoundError, ValidationError, ConflictError


class LessonService:
    """Contains business logic for Skills, Lessons, Exercises, and Lesson Sessions."""

    def __init__(self, db: Session):
        self.db = db
        self.repository = LessonRepository(db)
        self.gamification_service = GamificationService(db)

    def normalize_answer(self, answer: str, exercise_type: str) -> str:
        if not answer:
            return ""
        cleaned = answer.strip().lower()
        cleaned = re.sub(r"\s+", " ", cleaned)
        return cleaned

    def get_lesson_detail(self, lesson_id: str) -> LessonDetailResponse:
        lesson = self.repository.get_lesson_by_id(lesson_id)
        if not lesson:
            raise NotFoundError(f"Lesson with ID '{lesson_id}' was not found.")
        return LessonDetailResponse.model_validate(lesson)

    def start_lesson(
        self, current_user: UserModel, lesson_id: str
    ) -> LessonStartResponse:
        lesson = self.repository.get_lesson_by_id(lesson_id)
        if not lesson:
            raise NotFoundError(f"Lesson with ID '{lesson_id}' was not found.")

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
        user_answer: str,
    ) -> AnswerSubmissionResponse:
        # 1. Validate lesson exists
        lesson = self.repository.get_lesson_by_id(lesson_id)
        if not lesson:
            raise NotFoundError(f"Lesson with ID '{lesson_id}' was not found.")

        # 2. Validate exercise exists and belongs to lesson
        exercise = self.repository.get_exercise_by_id(exercise_id)
        if not exercise:
            raise NotFoundError(f"Exercise with ID '{exercise_id}' was not found.")
        if exercise.lesson_id != lesson_id:
            raise ValidationError(
                f"Exercise '{exercise_id}' does not belong to lesson '{lesson_id}'."
            )

        # 3. Validate lesson attempt
        attempt = self.repository.get_lesson_attempt_by_id(attempt_id)
        if not attempt:
            raise NotFoundError(f"Lesson attempt '{attempt_id}' was not found.")

        # 4. Verify user ownership
        if attempt.user_id != current_user.id:
            raise ValidationError("Lesson attempt belongs to another user.")

        # 5. Verify attempt belongs to lesson and is active
        if attempt.lesson_id != lesson_id:
            raise ValidationError(
                f"Lesson attempt '{attempt_id}' is not for lesson '{lesson_id}'."
            )
        if attempt.status != "started":
            raise ValidationError("LESSON_ATTEMPT_NOT_ACTIVE")

        # 6. Check duplicate answer submission (idempotency safety)
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
                hearts_lost=0,  # Duplicate submission does not deduct a second heart
                hearts_remaining=hearts_rem,
                attempt_completed=False,
            )

        # 7. Zero hearts check (reject answer if user has no hearts remaining)
        current_hearts = current_user.stats.hearts if current_user.stats else 5
        if current_hearts <= 0:
            raise ConflictError("You have no hearts remaining.", code="OUT_OF_HEARTS")

        # 8. Answer normalization & comparison
        norm_submission = self.normalize_answer(user_answer, exercise.type)
        norm_correct = self.normalize_answer(exercise.correct_answer, exercise.type)
        is_correct = norm_submission == norm_correct

        # 9. Transactional persistence & heart deduction
        try:
            hearts_lost = 0
            hearts_remaining = current_hearts

            if not is_correct:
                hearts_lost = 1
                hearts_remaining = self.gamification_service.deduct_heart(current_user.id)

            self.repository.create_exercise_attempt(
                lesson_attempt_id=attempt_id,
                exercise_id=exercise_id,
                answer=user_answer,
                is_correct=is_correct,
                hearts_lost=hearts_lost,
            )

            self.db.commit()

            return AnswerSubmissionResponse(
                exercise_id=exercise_id,
                is_correct=is_correct,
                correct_answer=exercise.correct_answer,
                hearts_lost=hearts_lost,
                hearts_remaining=hearts_remaining,
                attempt_completed=False,
            )
        except Exception:
            self.db.rollback()
            raise
