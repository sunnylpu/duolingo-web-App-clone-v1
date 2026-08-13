from sqlalchemy import (
    Column,
    String,
    Integer,
    Date,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship
from app.shared.database import Base


class UserStatsModel(Base):
    """
    UserStats database model tracking gamification statistics (1-to-1 with User).
    """
    __tablename__ = "user_stats"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(
        String,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    total_xp = Column(Integer, default=0, nullable=False)
    current_streak = Column(Integer, default=0, nullable=False)
    longest_streak = Column(Integer, default=0, nullable=False)
    hearts = Column(Integer, default=5, nullable=False)
    gems = Column(Integer, default=500, nullable=False)
    daily_goal_xp = Column(Integer, default=20, nullable=False)
    daily_xp = Column(Integer, default=0, nullable=False)
    last_active_date = Column(Date, nullable=True)
    last_heart_regeneration_at = Column(DateTime(timezone=True), nullable=True)
    last_practice_recovery_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    user = relationship("UserModel", back_populates="stats")


class AchievementModel(Base):
    """
    Achievement database model defining platform-wide badge/award criteria.
    """
    __tablename__ = "achievements"

    id = Column(String, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    icon = Column(String, nullable=False)
    requirement_type = Column(String, nullable=False)
    requirement_value = Column(Integer, nullable=False)

    # Relationships
    user_achievements = relationship(
        "UserAchievementModel",
        back_populates="achievement",
        cascade="all, delete-orphan",
    )


class UserAchievementModel(Base):
    """
    UserAchievement database model recording achievements unlocked by users.
    """
    __tablename__ = "user_achievements"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(
        String,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    achievement_id = Column(
        String,
        ForeignKey("achievements.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    earned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "achievement_id", name="uq_user_achievement"),
    )

    # Relationships
    user = relationship("UserModel", back_populates="user_achievements")
    achievement = relationship("AchievementModel", back_populates="user_achievements")
