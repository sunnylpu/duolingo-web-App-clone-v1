from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.course.repository import CourseRepository
from app.modules.progress.service import ProgressService
from app.modules.user.models import UserModel
from app.modules.course.schemas import (
    CourseSummaryResponse,
    CourseDetailResponse,
    PathResponse,
)
from app.shared.errors import NotFoundError


class CourseService:
    """Contains business logic for Courses and Learning Path generation."""

    def __init__(self, db: Session):
        self.db = db
        self.course_repo = CourseRepository(db)
        self.progress_service = ProgressService(db)

    def get_courses(self) -> List[CourseSummaryResponse]:
        courses = self.course_repo.get_courses()
        return [CourseSummaryResponse.model_validate(c) for c in courses]

    def get_course_detail(self, course_id: str) -> CourseDetailResponse:
        course = self.course_repo.get_course_by_id(course_id)
        if not course:
            raise NotFoundError(f"Course with ID '{course_id}' was not found.")
        return CourseDetailResponse.model_validate(course)

    def get_learning_path(
        self, current_user: UserModel, course_id: Optional[str] = None
    ) -> PathResponse:
        """Delegates learning path generation to ProgressService for single source of truth."""
        return self.progress_service.get_learning_path(current_user=current_user, course_id=course_id)
