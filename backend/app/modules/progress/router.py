from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.shared.database import get_db
from app.shared.security import get_current_user
from app.modules.user.models import UserModel
from app.modules.progress.repository import ProgressRepository
from app.modules.progress.service import ProgressService
from app.modules.progress.schemas import ProgressResponse

router = APIRouter(prefix="/progress", tags=["Progress"])


def get_progress_service(db: Session = Depends(get_db)) -> ProgressService:
    repository = ProgressRepository(db)
    return ProgressService(repository)


@router.get("", response_model=ProgressResponse, summary="Get user skill progress summary")
def get_user_progress(
    current_user: UserModel = Depends(get_current_user),
    service: ProgressService = Depends(get_progress_service),
):
    """Return a read-only progress summary for the current demo learner."""
    return service.get_user_progress_summary(current_user)
