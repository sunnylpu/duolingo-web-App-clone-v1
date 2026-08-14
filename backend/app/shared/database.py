import os
from typing import Generator
from sqlalchemy import create_engine, inspect, text, event
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


# Enforce SQLite foreign key integrity constraints
if settings.DATABASE_URL.startswith("sqlite"):
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

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
        UnitMilestoneModel,
        CourseMilestoneModel,
    )
    from app.modules.gamification.models import (  # noqa: F401
        UserStatsModel,
        AchievementModel,
        UserAchievementModel,
    )
    from app.modules.leaderboard.models import LeaderboardEntryModel  # noqa: F401
    from app.modules.social.models import UserFollowModel, ActivityEventModel  # noqa: F401
    from app.modules.quests.models import QuestModel, UserQuestModel  # noqa: F401
    from app.modules.notifications.models import (  # noqa: F401
        NotificationModel,
        NotificationPreferenceModel,
        NotificationDeliveryModel,
    )
    from app.shared.audit_models import AuditEventModel  # noqa: F401

    exec_engine = target_engine if target_engine is not None else engine

    if exec_engine != engine and settings.DATABASE_URL.startswith("sqlite"):
        @event.listens_for(exec_engine, "connect")
        def set_target_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    Base.metadata.create_all(bind=exec_engine)

    # Safe lightweight schema migration for newly added columns
    try:
        inspector = inspect(exec_engine)
        tables = inspector.get_table_names()
        if "achievements" in tables:
            columns = {c["name"] for c in inspector.get_columns("achievements")}
            with exec_engine.begin() as conn:
                if "category" not in columns:
                    conn.execute(text("ALTER TABLE achievements ADD COLUMN category VARCHAR DEFAULT 'learning'"))
                if "course_id" not in columns:
                    conn.execute(text("ALTER TABLE achievements ADD COLUMN course_id VARCHAR"))
                if "rarity" not in columns:
                    conn.execute(text("ALTER TABLE achievements ADD COLUMN rarity VARCHAR DEFAULT 'common'"))
                if "xp_reward" not in columns:
                    conn.execute(text("ALTER TABLE achievements ADD COLUMN xp_reward INTEGER DEFAULT 0"))

        if "users" in tables:
            user_columns = {c["name"] for c in inspector.get_columns("users")}
            with exec_engine.begin() as conn:
                if "password_hash" not in user_columns:
                    conn.execute(text("ALTER TABLE users ADD COLUMN password_hash VARCHAR(255)"))
                if "role" not in user_columns:
                    conn.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR(32) DEFAULT 'user'"))
    except Exception:
        pass


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
