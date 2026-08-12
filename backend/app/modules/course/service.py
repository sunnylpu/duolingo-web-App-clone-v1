from typing import List, Optional
from app.modules.course.repository import CourseRepository
from app.modules.course.models import CourseModel, UnitModel


class CourseService:
    """Contains business logic for the Course domain."""

    def __init__(self, repository: CourseRepository):
        self.repository = repository

    def list_courses(self) -> List[CourseModel]:
        return self.repository.get_courses()

    def get_course(self, course_id: str) -> Optional[CourseModel]:
        return self.repository.get_course_by_id(course_id)

    def list_course_units(self, course_id: str) -> List[UnitModel]:
        return self.repository.get_units_by_course(course_id)
