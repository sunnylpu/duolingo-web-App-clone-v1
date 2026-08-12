from sqlalchemy import Column, String, DateTime, func
from app.shared.database import Base


class CourseModel(Base):
    """Course database entity scaffolding."""
    __tablename__ = "courses"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    source_language = Column(String, nullable=False)
    target_language = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
