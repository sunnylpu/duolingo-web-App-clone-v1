from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.shared.database import Base


class LeaderboardEntryModel(Base):
    """
    LeaderboardEntry database model storing user rank standings for competitive periods.
    Periods: weekly, monthly, all_time.
    """
    __tablename__ = "leaderboard_entries"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(
        String,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    period = Column(String, default="weekly", nullable=False, index=True)
    xp = Column(Integer, default=0, nullable=False)
    rank = Column(Integer, default=1, nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    user = relationship("UserModel", back_populates="leaderboard_entries")
