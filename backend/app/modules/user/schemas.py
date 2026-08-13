from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr
from app.modules.gamification.schemas import GamificationStatsResponse


class UserBase(BaseModel):
    username: str
    display_name: str
    email: EmailStr
    avatar: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UserStatsResponse(BaseModel):
    total_xp: int
    current_streak: int
    longest_streak: int
    hearts: int
    gems: int
    daily_goal_xp: int
    daily_xp: int

    model_config = ConfigDict(from_attributes=True)


class LearningSummaryResponse(BaseModel):
    lessons_completed: int
    skills_completed: int
    skills_in_progress: int
    course_progress_percent: float

    model_config = ConfigDict(from_attributes=True)


class UserProfileResponse(BaseModel):
    user: UserResponse
    stats: GamificationStatsResponse
    learning: LearningSummaryResponse

    model_config = ConfigDict(from_attributes=True)
