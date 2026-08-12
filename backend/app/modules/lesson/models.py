from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import relationship
from app.shared.database import Base


class SkillModel(Base):
    """
    Skill database model representing a learning node within a unit.
    Supports prerequisite progression via self-referencing ForeignKey.
    """
    __tablename__ = "skills"

    id = Column(String, primary_key=True, index=True)
    unit_id = Column(
        String,
        ForeignKey("units.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    order_index = Column(Integer, default=1, nullable=False)
    xp_reward = Column(Integer, default=10, nullable=False)
    prerequisite_skill_id = Column(
        String,
        ForeignKey("skills.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    unit = relationship("UnitModel", back_populates="skills")
    prerequisite_skill = relationship("SkillModel", remote_side=[id])
    lessons = relationship(
        "LessonModel",
        back_populates="skill",
        cascade="all, delete-orphan",
        order_by="LessonModel.order_index",
    )
    progress_records = relationship(
        "SkillProgressModel",
        back_populates="skill",
        cascade="all, delete-orphan",
    )


class LessonModel(Base):
    """
    Lesson database model representing an individual learning module.
    """
    __tablename__ = "lessons"

    id = Column(String, primary_key=True, index=True)
    skill_id = Column(
        String,
        ForeignKey("skills.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    order_index = Column(Integer, default=1, nullable=False)
    xp_reward = Column(Integer, default=10, nullable=False)
    estimated_minutes = Column(Integer, default=5, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    skill = relationship("SkillModel", back_populates="lessons")
    exercises = relationship(
        "ExerciseModel",
        back_populates="lesson",
        cascade="all, delete-orphan",
        order_by="ExerciseModel.order_index",
    )
    attempts = relationship(
        "LessonAttemptModel",
        back_populates="lesson",
        cascade="all, delete-orphan",
    )


class ExerciseModel(Base):
    """
    Exercise database model supporting multiple exercise types via a flexible JSON data column.
    Types: multiple_choice, translate, word_bank, match_pairs, fill_blank, type_answer.
    """
    __tablename__ = "exercises"

    id = Column(String, primary_key=True, index=True)
    lesson_id = Column(
        String,
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    type = Column(String, nullable=False, index=True)
    prompt = Column(String, nullable=False)
    correct_answer = Column(String, nullable=False)
    data = Column(JSON, nullable=True)
    order_index = Column(Integer, default=1, nullable=False)
    xp_reward = Column(Integer, default=5, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    lesson = relationship("LessonModel", back_populates="exercises")
    attempts = relationship(
        "ExerciseAttemptModel",
        back_populates="exercise",
        cascade="all, delete-orphan",
    )
