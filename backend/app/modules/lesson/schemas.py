from typing import Optional, List, Any, Dict, Union
from datetime import datetime
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


class LessonStartResponse(BaseModel):
    attempt_id: Any
    lesson_id: str
    status: str
    started_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AnswerSubmissionRequest(BaseModel):
    attempt_id: Any
    answer: Union[str, Dict[str, Any], List[Any]]


class AnswerSubmissionResponse(BaseModel):
    exercise_id: str
    is_correct: bool
    correct_answer: str
    hearts_lost: int = 0
    hearts_remaining: int = 5
    attempt_completed: bool = False

    model_config = ConfigDict(from_attributes=True)
