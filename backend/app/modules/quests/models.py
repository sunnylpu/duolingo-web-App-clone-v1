import datetime
from typing import Optional
from sqlalchemy import String, Integer, Boolean, DateTime, Date, ForeignKey, UniqueConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.shared.database import Base


class QuestModel(Base):
    """Catalog of available daily and weekly quest templates."""

    __tablename__ = "quests"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(String(256), nullable=False)
    quest_type: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    # Types: LESSONS_COMPLETED, XP_EARNED, CORRECT_ANSWERS, SKILLS_COMPLETED, REVIEWS_COMPLETED
    target_value: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_xp: Mapped[int] = mapped_column(Integer, default=20, nullable=False)
    course_id: Mapped[Optional[str]] = mapped_column(String(64), ForeignKey("courses.id"), nullable=True)
    quest_scope: Mapped[str] = mapped_column(String(16), default="daily", nullable=False, index=True)  # "daily" or "weekly"

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow, nullable=False
    )


class UserQuestModel(Base):
    """Tracks learner progress and completion state for assigned quests."""

    __tablename__ = "user_quests"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
    quest_id: Mapped[str] = mapped_column(String(64), ForeignKey("quests.id"), nullable=False, index=True)
    current_value: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    completed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    reference_date: Mapped[datetime.date] = mapped_column(Date, nullable=False, index=True)

    user: Mapped["UserModel"] = relationship("UserModel")
    quest: Mapped["QuestModel"] = relationship("QuestModel")

    __table_args__ = (
        UniqueConstraint("user_id", "quest_id", "reference_date", name="uq_user_quest_refdate"),
    )
