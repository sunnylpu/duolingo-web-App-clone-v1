from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.shared.database import get_db
from app.modules.vocabulary.service import VocabularyService
from app.modules.vocabulary.schemas import VocabularyResponse

router = APIRouter(prefix="/vocabulary", tags=["Vocabulary"])


def get_vocabulary_service(db: Session = Depends(get_db)) -> VocabularyService:
    return VocabularyService(db)


@router.get("", response_model=VocabularyResponse, summary="Explore course vocabulary")
def get_vocabulary(
    course_id: Optional[str] = Query(None, description="Course ID filter"),
    topic: Optional[str] = Query(None, description="Topic category filter"),
    difficulty: Optional[int] = Query(None, ge=1, le=3, description="Difficulty level filter"),
    q: Optional[str] = Query(None, description="Word/translation search query"),
    service: VocabularyService = Depends(get_vocabulary_service),
):
    """Return categorized vocabulary items for a course with search & topic filters."""
    return service.get_course_vocabulary(
        course_id=course_id,
        topic=topic,
        difficulty=difficulty,
        query=q,
    )
