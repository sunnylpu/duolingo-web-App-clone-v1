from typing import Dict, Any
from pydantic import BaseModel, ConfigDict


class UsersOpsStats(BaseModel):
    total: int
    active_today: int


class CoursesOpsStats(BaseModel):
    total: int


class LearningOpsStats(BaseModel):
    lessons_completed_today: int
    exercises_answered_today: int
    correct_answer_pct: float


class GamificationOpsStats(BaseModel):
    xp_awarded_today: int
    achievements_unlocked_today: int


class SystemOpsStats(BaseModel):
    requests_total: int
    errors_total: int
    database_status: str
    version: str
    environment: str


class OpsOverviewResponse(BaseModel):
    users: UsersOpsStats
    courses: CoursesOpsStats
    learning: LearningOpsStats
    gamification: GamificationOpsStats
    system: SystemOpsStats

    model_config = ConfigDict(from_attributes=True)
