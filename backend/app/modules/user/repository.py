from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.user.models import UserModel


class UserRepository:
    """Handles database interactions for the User domain."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: str) -> Optional[UserModel]:
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[UserModel]:
        return self.db.query(UserModel).offset(skip).limit(limit).all()
