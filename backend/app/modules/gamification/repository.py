from typing import Optional
from sqlalchemy.orm import Session
from app.modules.gamification.models import GamificationModel


class GamificationRepository:
    """Handles data persistence for the Gamification domain."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_user_id(self, user_id: str) -> Optional[GamificationModel]:
        return self.db.query(GamificationModel).filter(GamificationModel.user_id == user_id).first()
