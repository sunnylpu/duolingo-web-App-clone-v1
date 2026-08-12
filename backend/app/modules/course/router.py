from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.shared.database import get_db
from app.modules.course.repository import CourseRepository
from app.modules.course.service import CourseService
from app.modules.course.schemas import CourseResponse

router = APIRouter(prefix="/courses", tags=["course"])


def get_course_service(db: Session = Depends(get_db)) -> CourseService:
    repository = CourseRepository(db)
    return CourseService(repository)


@router.get("", response_model=List[CourseResponse])
def list_courses(service: CourseService = Depends(get_course_service)):
    """List available courses (scaffolding)."""
    return service.list_courses()


@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: str, service: CourseService = Depends(get_course_service)):
    """Get course by ID (scaffolding)."""
    return service.get_course(course_id)
