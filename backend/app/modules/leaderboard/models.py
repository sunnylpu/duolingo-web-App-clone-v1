from sqlalchemy import Column, String, Integer, DateTime, func
from app.shared.database import Base


class LeaderboardModel(Base):
    """Leaderboard ranking database entity scaffolding."""
    __tablename__ = "leaderboards"

    id = Column(String, primary_key=True, index=True)
    league_name = Column(String, default="Bronze")
    user_id = Column(String, index=True, nullable=False)
    weekly_xp = Column(Integer, default=0)
    rank = Column(Integer, default=1)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
