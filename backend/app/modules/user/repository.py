from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.user.models import UserModel


class UserRepository:
    """Handles data persistence for the User domain."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: str) -> Optional[UserModel]:
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def get_by_username(self, username: str) -> Optional[UserModel]:
        return self.db.query(UserModel).filter(UserModel.username == username).first()

    def get_by_email(self, email: str) -> Optional[UserModel]:
        return self.db.query(UserModel).filter(UserModel.email == email).first()

    def create_or_update_user(
        self,
        user_id: str,
        username: str,
        display_name: str,
        email: str,
        avatar: Optional[str] = None,
        is_active: bool = True,
    ) -> UserModel:
        user = self.get_by_id(user_id) or self.get_by_username(username) or self.get_by_email(email)
        if not user:
            user = UserModel(
                id=user_id,
                username=username,
                display_name=display_name,
                email=email,
                avatar=avatar,
                is_active=is_active,
            )
            self.db.add(user)
        else:
            user.username = username
            user.display_name = display_name
            user.email = email
            user.avatar = avatar
            user.is_active = is_active

        self.db.commit()
        self.db.refresh(user)
        return user

    def get_all(self, skip: int = 0, limit: int = 100) -> List[UserModel]:
        return self.db.query(UserModel).offset(skip).limit(limit).all()
