from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class LeaderboardEntryResponse(BaseModel):
    rank: int
    user_id: str
    username: str
    display_name: str
    avatar: Optional[str] = None
    xp: int
    is_current_user: bool = False

    model_config = ConfigDict(from_attributes=True)


class LeaderboardResponse(BaseModel):
    period: str
    entries: List[LeaderboardEntryResponse] = []
    current_user_rank: Optional[int] = None
    total_participants: int = 0
    limit: int = 20
    offset: int = 0

    model_config = ConfigDict(from_attributes=True)


class UserRankResponse(BaseModel):
    period: str
    user_id: str
    rank: int
    xp: int
    total_participants: int

    model_config = ConfigDict(from_attributes=True)
