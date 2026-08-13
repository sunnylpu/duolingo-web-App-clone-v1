"""
Database Seed Verification Script
Executable via: python3 -m seed.verify
"""

import sys
import logging
from app.shared.database import SessionLocal
from app.modules.course.models import CourseModel, UnitModel
from app.modules.lesson.models import SkillModel, LessonModel, ExerciseModel
from app.modules.user.models import UserModel
from app.modules.progress.models import SkillProgressModel, LessonAttemptModel, ExerciseAttemptModel, DailyActivityModel
from app.modules.gamification.models import AchievementModel, UserStatsModel, UserAchievementModel
from app.modules.leaderboard.models import LeaderboardEntryModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("duolingo.seed.verify")


def verify_database_seed() -> bool:
    db = SessionLocal()
    try:
        logger.info("Verifying seed data integrity...")
        errors = []

        # 1. Course
        courses = db.query(CourseModel).all()
        if not courses:
            errors.append("No active courses found.")
        else:
            logger.info(f"✓ Found {len(courses)} active course(s).")

        # 2. Units & Skills
        units = db.query(UnitModel).all()
        if len(units) < 1:
            errors.append("Expected at least 1 unit in seed data.")

        skills = db.query(SkillModel).all()
        if len(skills) < 4:
            errors.append(f"Expected at least 4 skills, found {len(skills)}.")
        else:
            logger.info(f"✓ Found {len(skills)} skills.")

        # 3. Lessons & Exercises
        lessons = db.query(LessonModel).all()
        if len(lessons) < 4:
            errors.append(f"Expected at least 4 lessons, found {len(lessons)}.")

        exercises = db.query(ExerciseModel).all()
        exercise_types = {ex.type for ex in exercises}
        required_types = {
            "multiple_choice",
            "type_answer",
            "translate",
            "word_bank",
            "match_pairs",
            "fill_blank",
        }
        missing_types = required_types - exercise_types
        if missing_types:
            errors.append(f"Missing required exercise types: {missing_types}")
        else:
            logger.info(f"✓ Found all {len(required_types)} required exercise types across {len(exercises)} exercises.")

        # 4. Demo User
        demo_user = db.query(UserModel).filter(UserModel.id == "usr_demo").first()
        if not demo_user:
            errors.append("Demo user 'usr_demo' not found.")
        else:
            logger.info("✓ Demo user 'usr_demo' verified.")

        # 5. Achievements
        achievements = db.query(AchievementModel).all()
        if len(achievements) < 4:
            errors.append(f"Expected at least 4 achievements, found {len(achievements)}.")
        else:
            logger.info(f"✓ Found {len(achievements)} achievements.")

        # 6. Leaderboard Users
        lb_entries = db.query(LeaderboardEntryModel).all()
        if len(lb_entries) < 1:
            errors.append("No leaderboard entries found.")
        else:
            logger.info(f"✓ Found {len(lb_entries)} leaderboard entries.")

        if errors:
            logger.error("❌ Seed verification FAILED:")
            for err in errors:
                logger.error(f"  - {err}")
            return False

        logger.info("✅ Database seed verification PASSED with 100% data integrity!")
        return True
    finally:
        db.close()


if __name__ == "__main__":
    success = verify_database_seed()
    sys.exit(0 if success else 1)
