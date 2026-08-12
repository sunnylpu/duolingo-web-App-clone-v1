from typing import List, Optional
from app.modules.user.repository import UserRepository
from app.modules.user.models import UserModel


class UserService:
    """Encapsulates business logic for the User domain."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def list_users(self) -> List[UserModel]:
        return self.repository.get_all()

    def get_user_profile(self, user_id: str) -> Optional[UserModel]:
        return self.repository.get_by_id(user_id)
