from sqlalchemy import Column, String, Boolean, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.shared.database import Base


class CourseModel(Base):
    """
    Course database model (e.g. Spanish for English speakers).
    """
    __tablename__ = "courses"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, index=True, nullable=False)
    source_language = Column(String, nullable=False)
    target_language = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    units = relationship(
        "UnitModel",
        back_populates="course",
        cascade="all, delete-orphan",
        order_by="UnitModel.order_index",
    )


class UnitModel(Base):
    """
    Unit database model representing a thematic group of skills within a course.
    """
    __tablename__ = "units"

    id = Column(String, primary_key=True, index=True)
    course_id = Column(
        String,
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    order_index = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    course = relationship("CourseModel", back_populates="units")
    skills = relationship(
        "SkillModel",
        back_populates="unit",
        cascade="all, delete-orphan",
        order_by="SkillModel.order_index",
    )
