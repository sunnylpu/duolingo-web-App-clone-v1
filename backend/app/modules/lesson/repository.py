from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.lesson.models import LessonModel


class LessonRepository:
    """Handles data persistence for the Lesson domain."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, lesson_id: str) -> Optional[LessonModel]:
        return self.db.query(LessonModel).filter(LessonModel.id == lesson_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[LessonModel]:
        return self.db.query(LessonModel).offset(skip).limit(limit).all()
