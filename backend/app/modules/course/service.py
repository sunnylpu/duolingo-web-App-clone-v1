from typing import List, Optional
from app.modules.course.repository import CourseRepository
from app.modules.course.schemas import CourseResponse


class CourseService:
    """Contains business logic for the Course domain."""

    def __init__(self, repository: CourseRepository):
        self.repository = repository

    def list_courses(self) -> List[CourseResponse]:
        return [
            CourseResponse(id="crs_spanish", title="Spanish", source_language="en", target_language="es"),
            CourseResponse(id="crs_french", title="French", source_language="en", target_language="fr"),
        ]

    def get_course(self, course_id: str) -> Optional[CourseResponse]:
        return CourseResponse(id=course_id, title="Spanish", source_language="en", target_language="es")
