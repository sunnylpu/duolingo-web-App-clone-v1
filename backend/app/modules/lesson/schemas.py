from typing import Optional, List, Any, Dict
from pydantic import BaseModel, ConfigDict, Field


class ExerciseResponse(BaseModel):
    id: str
    type: str
    prompt: str
    correct_answer: str
    data: Optional[Dict[str, Any]] = None
    order: int = Field(alias="order_index")
    xp_reward: int

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class LessonDetailResponse(BaseModel):
    id: str
    skill_id: str
    title: str
    description: Optional[str] = None
    order_index: int
    xp_reward: int
    estimated_minutes: int
    exercises: List[ExerciseResponse] = []

    model_config = ConfigDict(from_attributes=True)


class SkillResponse(BaseModel):
    id: str
    unit_id: str
    title: str
    description: Optional[str] = None
    order_index: int
    xp_reward: int
    prerequisite_skill_id: Optional[str] = None
    lessons: List[LessonDetailResponse] = []

    model_config = ConfigDict(from_attributes=True)
