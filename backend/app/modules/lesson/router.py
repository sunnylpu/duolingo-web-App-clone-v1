from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.shared.database import get_db
from app.shared.security import get_current_user
from app.modules.user.models import UserModel
from app.modules.lesson.service import LessonService
from app.modules.lesson.schemas import (
    LessonDetailResponse,
    LessonStartResponse,
    AnswerSubmissionRequest,
    AnswerSubmissionResponse,
)

router = APIRouter(prefix="/lessons", tags=["Lessons"])


def get_lesson_service(db: Session = Depends(get_db)) -> LessonService:
    return LessonService(db)


@router.get("/{lesson_id}", response_model=LessonDetailResponse, summary="Get lesson and exercises")
def get_lesson(lesson_id: str, service: LessonService = Depends(get_lesson_service)):
    """Return detailed lesson information including all associated exercises."""
    return service.get_lesson_detail(lesson_id)


@router.post("/{lesson_id}/start", response_model=LessonStartResponse, summary="Start or resume a lesson attempt")
def start_lesson(
    lesson_id: str,
    current_user: UserModel = Depends(get_current_user),
    service: LessonService = Depends(get_lesson_service),
):
    """Transactional creation/resume of a lesson attempt for current user."""
    return service.start_lesson(current_user=current_user, lesson_id=lesson_id)


@router.post(
    "/{lesson_id}/exercises/{exercise_id}/answer",
    response_model=AnswerSubmissionResponse,
    summary="Submit exercise answer for validation",
)
def submit_exercise_answer(
    lesson_id: str,
    exercise_id: str,
    payload: AnswerSubmissionRequest,
    current_user: UserModel = Depends(get_current_user),
    service: LessonService = Depends(get_lesson_service),
):
    """Validate exercise answer, record ExerciseAttempt, and return feedback result."""
    return service.submit_exercise_answer(
        current_user=current_user,
        lesson_id=lesson_id,
        exercise_id=exercise_id,
        attempt_id=payload.attempt_id,
        user_answer=payload.answer,
    )
