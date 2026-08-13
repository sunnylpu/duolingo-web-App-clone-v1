"""
Database Reset Script
Executable via: python3 -m seed.reset
"""

import logging
from app.shared.database import engine, Base, SessionLocal
from app.modules.user.models import UserModel
from app.modules.course.models import CourseModel, UnitModel
from app.modules.lesson.models import SkillModel, LessonModel, ExerciseModel
from app.modules.progress.models import SkillProgressModel, LessonAttemptModel, ExerciseAttemptModel, DailyActivityModel
from app.modules.gamification.models import UserStatsModel, AchievementModel, UserAchievementModel
from app.modules.leaderboard.models import LeaderboardEntryModel
from seed.seed import seed_database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("duolingo.seed.reset")


def reset_database():
    logger.info("Dropping all existing database tables...")
    Base.metadata.drop_all(bind=engine)
    logger.info("All database tables dropped.")

    logger.info("Re-seeding database from scratch...")
    db = SessionLocal()
    try:
        counts = seed_database(db)
        logger.info(f"Database reset and re-seeding completed successfully: {counts}")
    finally:
        db.close()


if __name__ == "__main__":
    reset_database()
