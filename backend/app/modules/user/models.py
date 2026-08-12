from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.shared.database import Base


class UserModel(Base):
    """
    User database model representing a platform learner or admin.
    """
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    display_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    avatar = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    stats = relationship(
        "UserStatsModel",
        uselist=False,
        back_populates="user",
        cascade="all, delete-orphan",
    )
    skill_progress = relationship(
        "SkillProgressModel",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    lesson_attempts = relationship(
        "LessonAttemptModel",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    daily_activities = relationship(
        "DailyActivityModel",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    user_achievements = relationship(
        "UserAchievementModel",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    leaderboard_entries = relationship(
        "LeaderboardEntryModel",
        back_populates="user",
        cascade="all, delete-orphan",
    )
