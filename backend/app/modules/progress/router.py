from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.shared.database import get_db
from app.shared.security import get_current_user
from app.modules.user.models import UserModel
from app.modules.progress.repository import ProgressRepository
from app.modules.progress.service import ProgressService
from app.modules.progress.schemas import ProgressResponse
from app.modules.course.schemas import UnitProgressSummaryResponse

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


@router.get("/units", response_model=List[UnitProgressSummaryResponse], summary="Get user unit progress summary")
def get_user_unit_progress(
    course_id: Optional[str] = None,
    current_user: UserModel = Depends(get_current_user),
    service: ProgressService = Depends(get_progress_service),
):
    """Return unit progression metrics for the current user."""
    return service.get_user_unit_progress(current_user=current_user, course_id=course_id)
