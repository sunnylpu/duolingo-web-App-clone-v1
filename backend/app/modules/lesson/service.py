from typing import List, Optional
from app.modules.lesson.repository import LessonRepository
from app.modules.lesson.schemas import LessonDetailResponse
from app.shared.errors import NotFoundError


class LessonService:
    """Contains business logic for Skills, Lessons, and Exercises."""

    def __init__(self, repository: LessonRepository):
        self.repository = repository

    def get_lesson_detail(self, lesson_id: str) -> LessonDetailResponse:
        lesson = self.repository.get_lesson_by_id(lesson_id)
        if not lesson:
            raise NotFoundError(f"Lesson with ID '{lesson_id}' was not found.")
        return LessonDetailResponse.model_validate(lesson)
