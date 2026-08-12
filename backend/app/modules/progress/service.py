from typing import Optional
from app.modules.progress.repository import ProgressRepository
from app.modules.progress.schemas import ProgressResponse


class ProgressService:
    """Contains business logic for the Progress domain."""

    def __init__(self, repository: ProgressRepository):
        self.repository = repository

    def get_progress(self, user_id: str, course_id: str) -> ProgressResponse:
        return ProgressResponse(
            id="prg_01",
            user_id=user_id,
            course_id=course_id,
            completed_lessons=0,
        )
