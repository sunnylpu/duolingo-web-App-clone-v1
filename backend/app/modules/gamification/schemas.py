from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class GamificationStatsResponse(BaseModel):
    total_xp: int
    current_streak: int
    longest_streak: int
    hearts: int
    gems: int
    daily_goal_xp: int
    daily_xp: int

    model_config = ConfigDict(from_attributes=True)


class AchievementResponse(BaseModel):
    id: str
    code: str
    name: str
    description: str
    icon: str
    requirement_type: str
    requirement_value: int

    model_config = ConfigDict(from_attributes=True)


class UserAchievementResponse(BaseModel):
    achievement: AchievementResponse
    is_earned: bool
    earned_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
