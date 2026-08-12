from pydantic import BaseModel, ConfigDict


class GamificationBase(BaseModel):
    user_id: str
    xp: int
    streak_count: int
    hearts: int
    gems: int


class GamificationResponse(GamificationBase):
    id: str

    model_config = ConfigDict(from_attributes=True)
