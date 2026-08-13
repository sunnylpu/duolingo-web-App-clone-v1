from typing import Optional, List
from datetime import datetime, date
from pydantic import BaseModel, ConfigDict


class GamificationStatsResponse(BaseModel):
    total_xp: int
    current_streak: int
    longest_streak: int
    hearts: int
    gems: int
    daily_goal_xp: int
    daily_xp: int
    daily_goal_completed: bool = False
    activity_date: str = ""

    model_config = ConfigDict(from_attributes=True)


class DailyActivityResponse(BaseModel):
    date: str
    xp_earned: int
    lessons_completed: int
    goal_xp: int
    goal_completed: bool

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
    progress: int = 0
    target: int = 1

    model_config = ConfigDict(from_attributes=True)
