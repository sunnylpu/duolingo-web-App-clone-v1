from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.shared.database import get_db
from app.modules.lesson.repository import LessonRepository
from app.modules.lesson.service import LessonService
from app.modules.lesson.schemas import LessonResponse

router = APIRouter(prefix="/lessons", tags=["lesson"])


def get_lesson_service(db: Session = Depends(get_db)) -> LessonService:
    repository = LessonRepository(db)
    return LessonService(repository)


@router.get("", response_model=List[LessonResponse])
def list_lessons(service: LessonService = Depends(get_lesson_service)):
    """List lessons (scaffolding)."""
    return service.list_lessons()


@router.get("/{lesson_id}", response_model=LessonResponse)
def get_lesson(lesson_id: str, service: LessonService = Depends(get_lesson_service)):
    """Get lesson by ID (scaffolding)."""
    return service.get_lesson(lesson_id)
