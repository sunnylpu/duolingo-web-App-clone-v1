from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class SkillProgressSummary(BaseModel):
    skill_id: str
    status: str
    completion_percent: float
    crown_level: int
    lessons_completed: int
    xp_earned: int

    model_config = ConfigDict(from_attributes=True)


class ProgressResponse(BaseModel):
    skills: List[SkillProgressSummary] = []

    model_config = ConfigDict(from_attributes=True)
