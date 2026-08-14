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

    def get_courses(self, current_user: Optional[UserModel] = None) -> List[CourseSummaryResponse]:
        courses = self.course_repo.get_courses()
        results = []
        for c in courses:
            total_skills = sum(len(u.skills) for u in c.units)
            completed_skills = 0
            progress_pct = 0.0

            if current_user:
                path = self.progress_service.get_learning_path(current_user, course_id=c.id)
                all_skills = [s for u in path.units for s in u.skills]
                completed_skills = sum(1 for s in all_skills if s.status == "completed")
                if total_skills > 0:
                    progress_pct = round((completed_skills / total_skills) * 100, 1)

            resp = CourseSummaryResponse(
                id=c.id,
                name=c.name,
                code=c.code,
                source_language=c.source_language,
                target_language=c.target_language,
                description=c.description,
                is_active=c.is_active,
                total_skills=total_skills,
                completed_skills=completed_skills,
                progress_percent=progress_pct,
            )
            results.append(resp)
        return results

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
