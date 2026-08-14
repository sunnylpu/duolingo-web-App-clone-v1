from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.shared.database import get_db
from app.shared.security import get_current_user
from app.modules.user.models import UserModel
from app.modules.search.service import SearchService
from app.modules.search.schemas import SearchResponse

router = APIRouter(prefix="/search", tags=["Search"])


def get_search_service(db: Session = Depends(get_db)) -> SearchService:
    return SearchService(db)


@router.get("", response_model=SearchResponse, summary="Search curriculum content")
def search_curriculum(
    q: str = Query(..., min_length=1, description="Search query string"),
    course_id: Optional[str] = Query(None, description="Filter by course ID"),
    type: Optional[str] = Query(None, description="Filter by item type: course, unit, skill, lesson"),
    limit: int = Query(20, ge=1, le=100, description="Max results to return"),
    current_user: UserModel = Depends(get_current_user),
    service: SearchService = Depends(get_search_service),
):
    """Return normalized curriculum search results with relevance scoring."""
    return service.search_curriculum(
        query=q,
        current_user=current_user,
        course_id=course_id,
        item_type=type,
        limit=limit,
    )
