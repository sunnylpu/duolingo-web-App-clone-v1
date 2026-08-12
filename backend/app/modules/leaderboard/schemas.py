from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class LeaderboardEntryResponse(BaseModel):
    rank: int
    user_id: str
    username: str
    display_name: str
    avatar: Optional[str] = None
    xp: int

    model_config = ConfigDict(from_attributes=True)


class LeaderboardResponse(BaseModel):
    period: str
    entries: List[LeaderboardEntryResponse] = []

    model_config = ConfigDict(from_attributes=True)
