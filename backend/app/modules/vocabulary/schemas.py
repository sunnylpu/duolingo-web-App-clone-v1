from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class VocabularyItem(BaseModel):
    id: str
    word: str
    translation: str
    topic: str
    difficulty: int = 1
    course_id: str
    course_name: str
    skill_title: Optional[str] = None
    phonetic: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class VocabularyResponse(BaseModel):
    course_id: str
    total_items: int
    topics: List[str] = []
    items: List[VocabularyItem] = []

    model_config = ConfigDict(from_attributes=True)
