import datetime
from typing import Optional
from sqlalchemy import String, Boolean, DateTime, Date, ForeignKey, UniqueConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.shared.database import Base


class NotificationModel(Base):
    """Stores user notifications with deep-link metadata and read state."""

    __tablename__ = "notifications"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    # Types: DAILY_REMINDER, STREAK_REMINDER, QUEST_REMINDER, ACHIEVEMENT_UNLOCKED, UNIT_COMPLETED, COURSE_COMPLETED, SOCIAL_ACTIVITY
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    message: Mapped[str] = mapped_column(String(256), nullable=False)
    metadata_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow, nullable=False, index=True
    )

    user: Mapped["UserModel"] = relationship("UserModel")


class NotificationPreferenceModel(Base):
    """User preferences for controlling notification delivery categories."""

    __tablename__ = "notification_preferences"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), unique=True, nullable=False, index=True)
    daily_reminders: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    streak_reminders: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    quest_reminders: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    social_notifications: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    achievement_notifications: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False
    )

    user: Mapped["UserModel"] = relationship("UserModel")


class NotificationDeliveryModel(Base):
    """Deduplication ledger for automated daily & streak reminder deliveries."""

    __tablename__ = "notification_deliveries"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
    notification_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    reference_date: Mapped[datetime.date] = mapped_column(Date, nullable=False, index=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow, nullable=False
    )

    __table_args__ = (
        UniqueConstraint("user_id", "notification_type", "reference_date", name="uq_user_notif_delivery"),
    )
