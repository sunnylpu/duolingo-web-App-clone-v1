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

        # 2. English Flagship Course Verification
        en_course = db.query(CourseModel).filter(CourseModel.id == "crs_english").first()
        if en_course:
            en_units = db.query(UnitModel).filter(UnitModel.course_id == "crs_english").all()
            en_unit_ids = [u.id for u in en_units]
            en_skills = db.query(SkillModel).filter(SkillModel.unit_id.in_(en_unit_ids)).all() if en_unit_ids else []
            en_skill_ids = [s.id for s in en_skills]
            en_lessons = db.query(LessonModel).filter(LessonModel.skill_id.in_(en_skill_ids)).all() if en_skill_ids else []
            en_lesson_ids = [l.id for l in en_lessons]
            en_exercises = db.query(ExerciseModel).filter(ExerciseModel.lesson_id.in_(en_lesson_ids)).all() if en_lesson_ids else []

            logger.info(f"✓ English Flagship Course: {len(en_units)} units, {len(en_skills)} skills, {len(en_lessons)} lessons, {len(en_exercises)} exercises.")
            if len(en_units) < 8:
                errors.append(f"English course expected 8 units, found {len(en_units)}")
            if len(en_skills) < 32:
                errors.append(f"English course expected 32 skills, found {len(en_skills)}")
            if len(en_lessons) < 96:
                errors.append(f"English course expected 96 lessons, found {len(en_lessons)}")
            if len(en_exercises) < 576:
                errors.append(f"English course expected 576 exercises, found {len(en_exercises)}")

        # 3. Spanish Expanded Course Verification
        sp_course = db.query(CourseModel).filter(CourseModel.id == "crs_spanish").first()
        if sp_course:
            sp_units = db.query(UnitModel).filter(UnitModel.course_id == "crs_spanish").all()
            sp_unit_ids = [u.id for u in sp_units]
            sp_skills = db.query(SkillModel).filter(SkillModel.unit_id.in_(sp_unit_ids)).all() if sp_unit_ids else []
            sp_skill_ids = [s.id for s in sp_skills]
            sp_lessons = db.query(LessonModel).filter(LessonModel.skill_id.in_(sp_skill_ids)).all() if sp_skill_ids else []
            sp_lesson_ids = [l.id for l in sp_lessons]
            sp_exercises = db.query(ExerciseModel).filter(ExerciseModel.lesson_id.in_(sp_lesson_ids)).all() if sp_lesson_ids else []

            logger.info(f"✓ Spanish Expanded Course: {len(sp_units)} units, {len(sp_skills)} skills, {len(sp_lessons)} lessons, {len(sp_exercises)} exercises.")
            if len(sp_units) < 5:
                errors.append(f"Spanish course expected 5 units, found {len(sp_units)}")
            if len(sp_skills) < 20:
                errors.append(f"Spanish course expected 20 skills, found {len(sp_skills)}")
            if len(sp_lessons) < 60:
                errors.append(f"Spanish course expected 60 lessons, found {len(sp_lessons)}")
            if len(sp_exercises) < 360:
                errors.append(f"Spanish course expected 360 exercises, found {len(sp_exercises)}")

        # 4. Units & Skills General Count
        units = db.query(UnitModel).all()
        if len(units) < 1:
            errors.append("Expected at least 1 unit in seed data.")

        skills = db.query(SkillModel).all()
        if len(skills) < 4:
            errors.append(f"Expected at least 4 skills, found {len(skills)}.")
        else:
            logger.info(f"✓ Found {len(skills)} total skills across all courses.")

        # 5. Lessons & Exercises
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
            logger.info(f"✓ Found all {len(required_types)} required exercise types across {len(exercises)} total exercises.")

        # 6. Demo User
        demo_user = db.query(UserModel).filter(UserModel.id == "usr_demo").first()
        if not demo_user:
            errors.append("Demo user 'usr_demo' not found.")
        else:
            logger.info("✓ Demo user 'usr_demo' verified.")

        # 7. Achievements
        achievements = db.query(AchievementModel).all()
        if len(achievements) < 4:
            errors.append(f"Expected at least 4 achievements, found {len(achievements)}.")
        else:
            logger.info(f"✓ Found {len(achievements)} achievements.")

        # 8. Leaderboard Users
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
