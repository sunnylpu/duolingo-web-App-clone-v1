from typing import List, Optional
from app.modules.user.repository import UserRepository
from app.modules.user.models import UserModel
from app.modules.user.schemas import UserResponse, UserStatsResponse
from app.shared.errors import NotFoundError


class UserService:
    """Encapsulates business logic for the User domain."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_me(self, user: UserModel) -> UserResponse:
        return UserResponse.model_validate(user)

    def get_me_stats(self, user: UserModel) -> UserStatsResponse:
        if not user.stats:
            raise NotFoundError("User statistics not found for current user.")
        return UserStatsResponse.model_validate(user.stats)
