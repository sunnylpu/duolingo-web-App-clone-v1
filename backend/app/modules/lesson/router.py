from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.shared.database import get_db
from app.modules.lesson.repository import LessonRepository
from app.modules.lesson.service import LessonService
from app.modules.lesson.schemas import LessonDetailResponse

router = APIRouter(prefix="/lessons", tags=["Lessons"])


def get_lesson_service(db: Session = Depends(get_db)) -> LessonService:
    repository = LessonRepository(db)
    return LessonService(repository)


@router.get("/{lesson_id}", response_model=LessonDetailResponse, summary="Get lesson and exercises")
def get_lesson(lesson_id: str, service: LessonService = Depends(get_lesson_service)):
    """Return detailed lesson information including all associated exercises."""
    return service.get_lesson_detail(lesson_id)
