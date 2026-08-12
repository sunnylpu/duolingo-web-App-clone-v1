from sqlalchemy import Column, String, Integer, DateTime, func
from app.shared.database import Base


class LessonModel(Base):
    """Lesson database entity scaffolding."""
    __tablename__ = "lessons"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    order = Column(Integer, default=1)
    unit_id = Column(String, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
