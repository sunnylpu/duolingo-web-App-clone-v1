from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict


class SearchResultItem(BaseModel):
    id: str
    type: str  # "course", "unit", "skill", "lesson", "vocabulary"
    title: str
    description: Optional[str] = None
    course_id: Optional[str] = None
    course_name: Optional[str] = None
    unit_id: Optional[str] = None
    skill_id: Optional[str] = None
    status: Optional[str] = None
    progress_percent: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)


class SearchResponse(BaseModel):
    query: str
    total_results: int
    results: List[SearchResultItem] = []

    model_config = ConfigDict(from_attributes=True)
