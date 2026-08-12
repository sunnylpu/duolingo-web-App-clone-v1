from sqlalchemy import Column, String, Integer, DateTime, func
from app.shared.database import Base


class GamificationModel(Base):
    """Gamification database entity scaffolding (XP, Streaks, Hearts)."""
    __tablename__ = "gamification"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True, nullable=False)
    xp = Column(Integer, default=0)
    streak_count = Column(Integer, default=0)
    hearts = Column(Integer, default=5)
    gems = Column(Integer, default=500)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
