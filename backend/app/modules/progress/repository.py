from typing import Optional
from sqlalchemy.orm import Session
from app.modules.progress.models import ProgressModel


class ProgressRepository:
    """Handles data persistence for the Progress domain."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_user_and_course(self, user_id: str, course_id: str) -> Optional[ProgressModel]:
        return (
            self.db.query(ProgressModel)
            .filter(ProgressModel.user_id == user_id, ProgressModel.course_id == course_id)
            .first()
        )
