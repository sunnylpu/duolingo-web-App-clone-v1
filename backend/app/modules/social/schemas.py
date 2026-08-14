from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class UserSocialSummary(BaseModel):
    id: str
    username: str
    display_name: str
    avatar: str
    total_xp: int = 0
    current_streak: int = 0
    is_following: bool = False

    model_config = ConfigDict(from_attributes=True)


class SocialStatsResponse(BaseModel):
    followers_count: int
    following_count: int

    model_config = ConfigDict(from_attributes=True)


class ActivityEventResponse(BaseModel):
    id: str
    user: UserSocialSummary
    event_type: str
    message: str
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ActivityFeedResponse(BaseModel):
    items: List[ActivityEventResponse] = []
    total: int = 0

    model_config = ConfigDict(from_attributes=True)


class PublicProfileResponse(BaseModel):
    id: str
    username: str
    display_name: str
    avatar: str
    total_xp: int
    current_streak: int
    longest_streak: int
    followers_count: int
    following_count: int
    is_following: bool = False

    model_config = ConfigDict(from_attributes=True)


class FriendSuggestionResponse(BaseModel):
    user: UserSocialSummary
    reason: str = "Leaderboard contender"

    model_config = ConfigDict(from_attributes=True)
