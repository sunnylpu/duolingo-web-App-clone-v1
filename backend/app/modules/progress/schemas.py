from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict


class SkillProgressSummary(BaseModel):
    skill_id: str
    status: str
    completion_percent: float
    crown_level: int
    lessons_completed: int
    xp_earned: int
    prerequisite_skill_id: Optional[str] = None
    prerequisite_title: Optional[str] = None
    accuracy_percent: float = 100.0
    mastery_score: float = 0.0
    mastery_state: str = "weak"

    model_config = ConfigDict(from_attributes=True)


class ProgressResponse(BaseModel):
    skills: List[SkillProgressSummary] = []

    model_config = ConfigDict(from_attributes=True)


class SkillPerformanceResponse(BaseModel):
    skill_id: str
    title: str
    completion_percent: float
    accuracy_percent: float
    mastery_score: float
    mastery_state: str  # weak, developing, strong, mastered
    attempts: int
    correct: int
    incorrect: int
    recommended_difficulty: int

    model_config = ConfigDict(from_attributes=True)


class ReviewSkillSummary(BaseModel):
    skill_id: str
    title: str
    accuracy_percent: float
    reason: str


class ReviewExerciseDetail(BaseModel):
    id: str
    type: str
    prompt: str
    correct_answer: str
    data: Optional[Dict[str, Any]] = None
    order_index: int = 1
    xp_reward: int = 0
    skill_id: str
    previous_user_answer: Optional[str] = None


class ReviewResponse(BaseModel):
    available: bool
    count: int
    skills: List[ReviewSkillSummary] = []
    exercises: List[ReviewExerciseDetail] = []

    model_config = ConfigDict(from_attributes=True)
