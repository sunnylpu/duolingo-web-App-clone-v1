from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.shared.database import get_db
from app.shared.security import get_current_user
from app.modules.user.models import UserModel
from app.modules.course.service import CourseService
from app.modules.course.schemas import (
    CourseSummaryResponse,
    CourseDetailResponse,
    PathResponse,
)

router = APIRouter(tags=["Courses"])


def get_course_service(db: Session = Depends(get_db)) -> CourseService:
    return CourseService(db)


@router.get("/courses", response_model=List[CourseSummaryResponse], summary="List available courses")
def list_courses(service: CourseService = Depends(get_course_service)):
    """Return all active language courses."""
    return service.get_courses()


@router.get("/courses/{course_id}", response_model=CourseDetailResponse, summary="Get course details")
def get_course(course_id: str, service: CourseService = Depends(get_course_service)):
    """Return detailed information for a specific course, including units."""
    return service.get_course_detail(course_id)


# Path Router for GET /api/v1/path
path_router = APIRouter(prefix="/path", tags=["Learning Path"])


@path_router.get("", response_model=PathResponse, summary="Get current user learning path")
def get_learning_path(
    course_id: Optional[str] = None,
    current_user: UserModel = Depends(get_current_user),
    service: CourseService = Depends(get_course_service),
):
    """Return the structured learning path (Units -> Skills -> Progress Status) for the current user."""
    return service.get_learning_path(current_user, course_id=course_id)
