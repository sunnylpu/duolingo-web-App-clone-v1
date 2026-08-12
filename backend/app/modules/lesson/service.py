from typing import List, Optional
from app.modules.lesson.repository import LessonRepository
from app.modules.lesson.schemas import LessonResponse


class LessonService:
    """Contains business logic for the Lesson domain."""

    def __init__(self, repository: LessonRepository):
        self.repository = repository

    def list_lessons(self) -> List[LessonResponse]:
        return [
            LessonResponse(id="lsn_01", title="Basics 1", order=1, unit_id="unit_01"),
            LessonResponse(id="lsn_02", title="Greetings", order=2, unit_id="unit_01"),
        ]

    def get_lesson(self, lesson_id: str) -> Optional[LessonResponse]:
        return LessonResponse(id=lesson_id, title="Basics 1", order=1, unit_id="unit_01")
