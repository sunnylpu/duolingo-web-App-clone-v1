from pydantic import BaseModel, ConfigDict


class LeaderboardEntry(BaseModel):
    user_id: str
    username: str
    weekly_xp: int
    rank: int


class LeaderboardResponse(BaseModel):
    league_name: str
    entries: list[LeaderboardEntry]

    model_config = ConfigDict(from_attributes=True)
