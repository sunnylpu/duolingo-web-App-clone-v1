from sqlalchemy import Column, String, Integer, DateTime, func
from app.shared.database import Base


class ProgressModel(Base):
    """User progress database entity scaffolding."""
    __tablename__ = "user_progress"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    course_id = Column(String, index=True, nullable=False)
    completed_lessons = Column(Integer, default=0)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
