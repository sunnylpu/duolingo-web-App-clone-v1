import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from app.config import settings


class Base(DeclarativeBase):
    """Declarative Base class for all SQLAlchemy domain models."""
    pass


# Ensure data directory exists if using local SQLite database file
if settings.DATABASE_URL.startswith("sqlite"):
    db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    if "/" in db_path:
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

engine_kwargs = {}
if settings.DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(settings.DATABASE_URL, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db(target_engine=None) -> None:
    """
    Central database initialization mechanism.
    Imports all domain models and creates relational database tables.
    """
    # Import all domain models to ensure they are registered with Base.metadata
    from app.modules.user.models import UserModel  # noqa: F401
    from app.modules.course.models import CourseModel, UnitModel  # noqa: F401
    from app.modules.lesson.models import (  # noqa: F401
        SkillModel,
        LessonModel,
        ExerciseModel,
    )
    from app.modules.progress.models import (  # noqa: F401
        SkillProgressModel,
        LessonAttemptModel,
        ExerciseAttemptModel,
        DailyActivityModel,
    )
    from app.modules.gamification.models import (  # noqa: F401
        UserStatsModel,
        AchievementModel,
        UserAchievementModel,
    )
    from app.modules.leaderboard.models import LeaderboardEntryModel  # noqa: F401

    exec_engine = target_engine if target_engine is not None else engine
    Base.metadata.create_all(bind=exec_engine)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency yielding a clean database session per request.
    Ensures proper session closure upon request completion.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
