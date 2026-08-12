from typing import Optional, List, Any, Dict
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ExerciseResponse(BaseModel):
    id: str
    lesson_id: str
    type: str
    prompt: str
    correct_answer: str
    data: Optional[Dict[str, Any]] = None
    order_index: int
    xp_reward: int

    model_config = ConfigDict(from_attributes=True)


class LessonResponse(BaseModel):
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
    lessons: List[LessonResponse] = []

    model_config = ConfigDict(from_attributes=True)
