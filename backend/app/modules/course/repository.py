from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.course.models import CourseModel


class CourseRepository:
    """Handles data persistence for the Course domain."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, course_id: str) -> Optional[CourseModel]:
        return self.db.query(CourseModel).filter(CourseModel.id == course_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[CourseModel]:
        return self.db.query(CourseModel).offset(skip).limit(limit).all()
