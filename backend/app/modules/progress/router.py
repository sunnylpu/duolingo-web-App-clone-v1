from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.shared.database import get_db
from app.modules.progress.repository import ProgressRepository
from app.modules.progress.service import ProgressService
from app.modules.progress.schemas import ProgressResponse

router = APIRouter(prefix="/progress", tags=["progress"])


def get_progress_service(db: Session = Depends(get_db)) -> ProgressService:
    repository = ProgressRepository(db)
    return ProgressService(repository)


@router.get("/{user_id}/{course_id}", response_model=ProgressResponse)
def get_user_progress(
    user_id: str,
    course_id: str,
    service: ProgressService = Depends(get_progress_service),
):
    """Retrieve user progress for a course (scaffolding)."""
    return service.get_progress(user_id, course_id)
