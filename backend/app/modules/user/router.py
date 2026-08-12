from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.shared.database import get_db
from app.modules.user.repository import UserRepository
from app.modules.user.service import UserService
from app.modules.user.schemas import UserResponse

router = APIRouter(prefix="/users", tags=["user"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repository = UserRepository(db)
    return UserService(repository)


@router.get("", response_model=List[UserResponse])
def list_users(service: UserService = Depends(get_user_service)):
    """Retrieve list of users (scaffolding)."""
    return service.list_users()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, service: UserService = Depends(get_user_service)):
    """Retrieve user by ID (scaffolding)."""
    return service.get_user_profile(user_id)
