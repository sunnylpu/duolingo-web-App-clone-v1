from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.shared.database import get_db
from app.shared.security import get_current_user
from app.modules.user.models import UserModel
from app.modules.progress.repository import ProgressRepository
from app.modules.progress.service import ProgressService
from app.modules.progress.schemas import (
    ProgressResponse,
    SkillPerformanceResponse,
    ReviewResponse,
)
from app.modules.course.schemas import UnitProgressSummaryResponse, CourseProgressSummaryResponse

router = APIRouter(tags=["Progress"])


def get_progress_service(db: Session = Depends(get_db)) -> ProgressService:
    repository = ProgressRepository(db)
    return ProgressService(repository)


@router.get("/progress", response_model=ProgressResponse, summary="Get user skill progress summary")
def get_user_progress(
    current_user: UserModel = Depends(get_current_user),
    service: ProgressService = Depends(get_progress_service),
):
    """Return a read-only progress summary for the current demo learner."""
    return service.get_user_progress_summary(current_user)


@router.get("/progress/units", response_model=List[UnitProgressSummaryResponse], summary="Get user unit progress summary")
def get_user_unit_progress(
    course_id: Optional[str] = None,
    current_user: UserModel = Depends(get_current_user),
    service: ProgressService = Depends(get_progress_service),
):
    """Return unit progression metrics for the current user."""
    return service.get_user_unit_progress(current_user=current_user, course_id=course_id)


@router.get("/progress/course/{course_id}", response_model=CourseProgressSummaryResponse, summary="Get user course progress summary")
def get_user_course_progress(
    course_id: str,
    current_user: UserModel = Depends(get_current_user),
    service: ProgressService = Depends(get_progress_service),
):
    """Return top-level course progression summary for the specified course."""
    return service.get_user_course_progress(current_user=current_user, course_id=course_id)


@router.get("/progress/skills/{skill_id}", response_model=SkillPerformanceResponse, summary="Get skill performance analytics")
def get_skill_performance(
    skill_id: str,
    current_user: UserModel = Depends(get_current_user),
    service: ProgressService = Depends(get_progress_service),
):
    """Return detailed performance analytics, accuracy, and mastery state for a skill."""
    return service.get_skill_performance(current_user=current_user, skill_id=skill_id)


@router.get("/review", response_model=ReviewResponse, summary="Get Smart Review exercises")
def get_smart_review(
    course_id: Optional[str] = None,
    current_user: UserModel = Depends(get_current_user),
    service: ProgressService = Depends(get_progress_service),
):
    """Return adaptive review recommendations based on recent mistakes and skill accuracy."""
    return service.get_smart_review(current_user=current_user, course_id=course_id)
