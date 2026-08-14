"""
Deterministic & Idempotent Database Seed Script.
Executable via: python -m seed.seed
"""

import logging
from sqlalchemy.orm import Session
from app.shared.database import SessionLocal, init_db
from app.modules.user.repository import UserRepository
from app.modules.course.repository import CourseRepository
from app.modules.lesson.repository import LessonRepository
from app.modules.progress.repository import ProgressRepository
from app.modules.gamification.repository import GamificationRepository
from app.modules.leaderboard.repository import LeaderboardRepository

from seed.generators.course_generator import generate_course
from seed.catalogs import ALL_COURSE_SPECS
from seed.achievement_data import ACHIEVEMENTS
from seed.user_data import (
    DEMO_USER,
    DEMO_USER_STATS,
    LEADERBOARD_USERS,
    DEMO_SKILL_PROGRESSIONS,
    get_demo_daily_activities,
)

logger = logging.getLogger("duolingo.seed")


def seed_database(db: Session) -> dict:
    """
    Populates database with deterministic seed data in an idempotent manner.
    Returns dictionary with counts of seeded entities.
    """
    logger.info("Initializing database schemas...")
    init_db()

    user_repo = UserRepository(db)
    course_repo = CourseRepository(db)
    lesson_repo = LessonRepository(db)
    progress_repo = ProgressRepository(db)
    gamification_repo = GamificationRepository(db)
    leaderboard_repo = LeaderboardRepository(db)

    counts = {
        "courses": 0,
        "units": 0,
        "skills": 0,
        "lessons": 0,
        "exercises": 0,
        "users": 0,
        "achievements": 0,
        "leaderboard_entries": 0,
    }

    # 1. Seed Achievements
    for ach in ACHIEVEMENTS:
        gamification_repo.create_achievement(
            achievement_id=ach["id"],
            code=ach["code"],
            name=ach["name"],
            description=ach["description"],
            icon=ach["icon"],
            requirement_type=ach["requirement_type"],
            requirement_value=ach["requirement_value"],
        )
        counts["achievements"] += 1

    # 2. Seed Courses (English flagship + Spanish expanded + French secondary)
    courses_to_seed = [generate_course(spec) for spec in ALL_COURSE_SPECS]

    for c_data in courses_to_seed:
        course_repo.create_or_update_course(
            course_id=c_data["id"],
            name=c_data["name"],
            code=c_data["code"],
            source_language=c_data["source_language"],
            target_language=c_data["target_language"],
            description=c_data["description"],
        )
        counts["courses"] += 1

        for unit_data in c_data["units"]:
            course_repo.create_or_update_unit(
                unit_id=unit_data["id"],
                course_id=c_data["id"],
                title=unit_data["title"],
                description=unit_data["description"],
                order_index=unit_data["order_index"],
            )
            counts["units"] += 1

            for skill_data in unit_data["skills"]:
                lesson_repo.create_or_update_skill(
                    skill_id=skill_data["id"],
                    unit_id=unit_data["id"],
                    title=skill_data["title"],
                    description=skill_data["description"],
                    order_index=skill_data["order_index"],
                    xp_reward=skill_data["xp_reward"],
                    prerequisite_skill_id=skill_data["prerequisite_skill_id"],
                )
                counts["skills"] += 1

                for lsn_data in skill_data["lessons"]:
                    lesson_repo.create_or_update_lesson(
                        lesson_id=lsn_data["id"],
                        skill_id=skill_data["id"],
                        title=lsn_data["title"],
                        description=lsn_data["description"],
                        order_index=lsn_data["order_index"],
                        xp_reward=lsn_data["xp_reward"],
                        estimated_minutes=lsn_data["estimated_minutes"],
                    )
                    counts["lessons"] += 1

                    for ex_data in lsn_data["exercises"]:
                        lesson_repo.create_or_update_exercise(
                            exercise_id=ex_data["id"],
                            lesson_id=lsn_data["id"],
                            type=ex_data["type"],
                            prompt=ex_data["prompt"],
                            correct_answer=ex_data["correct_answer"],
                            data=ex_data["data"],
                            order_index=ex_data["order_index"],
                            xp_reward=ex_data["xp_reward"],
                        )
                        counts["exercises"] += 1

    # 3. Seed Demo Learner User & UserStats
    user_repo.create_or_update_user(
        user_id=DEMO_USER["id"],
        username=DEMO_USER["username"],
        display_name=DEMO_USER["display_name"],
        email=DEMO_USER["email"],
        avatar=DEMO_USER["avatar"],
    )
    counts["users"] += 1

    gamification_repo.create_or_update_user_stats(
        stats_id=DEMO_USER_STATS["id"],
        user_id=DEMO_USER["id"],
        total_xp=DEMO_USER_STATS["total_xp"],
        current_streak=DEMO_USER_STATS["current_streak"],
        longest_streak=DEMO_USER_STATS["longest_streak"],
        hearts=DEMO_USER_STATS["hearts"],
        gems=DEMO_USER_STATS["gems"],
        daily_goal_xp=DEMO_USER_STATS["daily_goal_xp"],
        daily_xp=DEMO_USER_STATS["daily_xp"],
    )

    # 4. Seed Demo Skill Progressions
    for prg in DEMO_SKILL_PROGRESSIONS:
        progress_repo.upsert_skill_progress(
            progress_id=prg["id"],
            user_id=prg["user_id"],
            skill_id=prg["skill_id"],
            status=prg["status"],
            completion_percent=prg["completion_percent"],
            crown_level=prg["crown_level"],
            lessons_completed=prg["lessons_completed"],
            xp_earned=prg["xp_earned"],
        )

    # 5. Seed Demo Daily Activity Records
    for act in get_demo_daily_activities():
        progress_repo.record_daily_activity(
            activity_id=act["id"],
            user_id=act["user_id"],
            activity_date=act["activity_date"],
            xp_earned=act["xp_earned"],
            lessons_completed=act["lessons_completed"],
            minutes_learned=act["minutes_learned"],
            goal_completed=act["goal_completed"],
        )

    # 6. Grant Initial Demo Achievements
    ach_first = gamification_repo.get_achievement_by_code("FIRST_LESSON")
    if ach_first:
        gamification_repo.grant_user_achievement(
            user_achievement_id="uach_demo_1",
            user_id=DEMO_USER["id"],
            achievement_id=ach_first.id,
        )
    ach_100 = gamification_repo.get_achievement_by_code("100_XP")
    if ach_100:
        gamification_repo.grant_user_achievement(
            user_achievement_id="uach_demo_2",
            user_id=DEMO_USER["id"],
            achievement_id=ach_100.id,
        )

    # 7. Seed Demo Leaderboard Users & Entries
    leaderboard_repo.create_or_update_entry(
        entry_id="lb_demo_weekly",
        user_id=DEMO_USER["id"],
        period="weekly",
        xp=DEMO_USER_STATS["total_xp"],
        rank=4,
    )
    counts["leaderboard_entries"] += 1

    for lb_usr in LEADERBOARD_USERS:
        user_repo.create_or_update_user(
            user_id=lb_usr["id"],
            username=lb_usr["username"],
            display_name=lb_usr["display_name"],
            email=lb_usr["email"],
            avatar=lb_usr["avatar"],
        )
        counts["users"] += 1

        leaderboard_repo.create_or_update_entry(
            entry_id=f"lb_{lb_usr['id']}_weekly",
            user_id=lb_usr["id"],
            period="weekly",
            xp=lb_usr["xp"],
            rank=lb_usr["rank"],
        )
        counts["leaderboard_entries"] += 1

    logger.info("Database seeding completed successfully.")
    return counts


if __name__ == "__main__":
    db = SessionLocal()
    try:
        results = seed_database(db)
        print("Seed Summary:", results)
    finally:
        db.close()
