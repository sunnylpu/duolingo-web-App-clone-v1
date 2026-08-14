from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.shared.database import get_db
from app.shared.security import get_current_user
from app.modules.user.models import UserModel
from app.modules.home.service import HomeService
from app.modules.home.schemas import HomeDashboardResponse

router = APIRouter(prefix="/home", tags=["Home"])


def get_home_service(db: Session = Depends(get_db)) -> HomeService:
    return HomeService(db)


@router.get("", response_model=HomeDashboardResponse, summary="Get learner home dashboard aggregation")
def get_home_dashboard(
    course_id: Optional[str] = None,
    current_user: UserModel = Depends(get_current_user),
    service: HomeService = Depends(get_home_service),
):
    """BFF-style aggregated learner dashboard for the home view."""
    return service.get_home_dashboard(current_user=current_user, course_id=course_id)
