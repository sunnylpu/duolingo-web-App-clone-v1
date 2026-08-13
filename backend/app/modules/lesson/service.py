from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.lesson.repository import LessonRepository
from app.modules.lesson.schemas import LessonDetailResponse, LessonStartResponse
from app.modules.user.models import UserModel
from app.shared.errors import NotFoundError


class LessonService:
    """Contains business logic for Skills, Lessons, Exercises, and Lesson Sessions."""

    def __init__(self, db: Session):
        self.db = db
        self.repository = LessonRepository(db)

    def get_lesson_detail(self, lesson_id: str) -> LessonDetailResponse:
        lesson = self.repository.get_lesson_by_id(lesson_id)
        if not lesson:
            raise NotFoundError(f"Lesson with ID '{lesson_id}' was not found.")
        return LessonDetailResponse.model_validate(lesson)

    def start_lesson(
        self, current_user: UserModel, lesson_id: str
    ) -> LessonStartResponse:
        # Verify lesson exists
        lesson = self.repository.get_lesson_by_id(lesson_id)
        if not lesson:
            raise NotFoundError(f"Lesson with ID '{lesson_id}' was not found.")

        # Check for active existing attempt to prevent duplicate attempt records
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

        # Transactional creation of new LessonAttempt
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
