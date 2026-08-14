from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship
from app.shared.database import Base


class SkillProgressModel(Base):
    """
    SkillProgress model tracking user's learning status and mastery per skill.
    Statuses: locked, available, in_progress, completed.
    """
    __tablename__ = "skill_progress"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(
        String,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    skill_id = Column(
        String,
        ForeignKey("skills.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status = Column(String, default="locked", nullable=False)
    completion_percent = Column(Float, default=0.0, nullable=False)
    crown_level = Column(Integer, default=0, nullable=False)
    lessons_completed = Column(Integer, default=0, nullable=False)
    xp_earned = Column(Integer, default=0, nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("user_id", "skill_id", name="uq_user_skill_progress"),
    )

    # Relationships
    user = relationship("UserModel", back_populates="skill_progress")
    skill = relationship("SkillModel", back_populates="progress_records")


class LessonAttemptModel(Base):
    """
    LessonAttempt model recording user sessions on individual lessons.
    Statuses: started, completed, failed, abandoned.
    """
    __tablename__ = "lesson_attempts"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(
        String,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    lesson_id = Column(
        String,
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, default="started", nullable=False)
    score = Column(Integer, default=0, nullable=False)
    xp_earned = Column(Integer, default=0, nullable=False)
    hearts_lost = Column(Integer, default=0, nullable=False)

    # Relationships
    user = relationship("UserModel", back_populates="lesson_attempts")
    lesson = relationship("LessonModel", back_populates="attempts")
    exercise_attempts = relationship(
        "ExerciseAttemptModel",
        back_populates="lesson_attempt",
        cascade="all, delete-orphan",
    )


class ExerciseAttemptModel(Base):
    """
    ExerciseAttempt model recording individual answers within a lesson session.
    """
    __tablename__ = "exercise_attempts"

    id = Column(String, primary_key=True, index=True)
    lesson_attempt_id = Column(
        String,
        ForeignKey("lesson_attempts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    exercise_id = Column(
        String,
        ForeignKey("exercises.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    answer = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    hearts_lost = Column(Integer, default=0, nullable=False)
    answered_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("lesson_attempt_id", "exercise_id", name="uq_lesson_attempt_exercise"),
    )

    # Relationships
    lesson_attempt = relationship("LessonAttemptModel", back_populates="exercise_attempts")
    exercise = relationship("ExerciseModel", back_populates="attempts")


class DailyActivityModel(Base):
    """
    DailyActivity model tracking daily user engagement metrics for streaks and activity graphs.
    """
    __tablename__ = "daily_activities"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(
        String,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    activity_date = Column(Date, nullable=False, index=True)
    xp_earned = Column(Integer, default=0, nullable=False)
    lessons_completed = Column(Integer, default=0, nullable=False)
    minutes_learned = Column(Integer, default=0, nullable=False)
    goal_completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "activity_date", name="uq_user_daily_activity"),
    )

    # Relationships
    user = relationship("UserModel", back_populates="daily_activities")


class UnitMilestoneModel(Base):
    """
    UnitMilestone model recording durable unit completions and milestone rewards.
    Prevents duplicate unit completion rewards.
    """
    __tablename__ = "unit_milestones"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(
        String,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    unit_id = Column(
        String,
        ForeignKey("units.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    reward_xp = Column(Integer, default=50, nullable=False)
    completed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "unit_id", name="uq_user_unit_milestone"),
    )

    # Relationships
    user = relationship("UserModel")
    unit = relationship("UnitModel")


class CourseMilestoneModel(Base):
    """
    CourseMilestone model recording durable top-level course completions and mastery rewards.
    Prevents duplicate course completion rewards (+500 XP).
    """
    __tablename__ = "course_milestones"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(
        String,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    course_id = Column(
        String,
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    reward_xp = Column(Integer, default=500, nullable=False)
    completed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "course_id", name="uq_user_course_milestone"),
    )

    # Relationships
    user = relationship("UserModel")
    course = relationship("CourseModel")
