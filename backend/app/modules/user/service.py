from typing import List, Optional
from app.modules.user.repository import UserRepository
from app.modules.user.schemas import UserResponse


class UserService:
    """Encapsulates business logic for the User domain."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def list_users(self) -> List[UserResponse]:
        # Phase 01 architectural placeholder logic
        return [
            UserResponse(id="usr_01", email="learner@example.com", username="learner1", is_active=True)
        ]

    def get_user_profile(self, user_id: str) -> Optional[UserResponse]:
        return UserResponse(id=user_id, email="learner@example.com", username="learner1", is_active=True)
