from datetime import date, timedelta
from app.shared.security import hash_password

DEMO_USER = {
    "id": "usr_demo",
    "username": "demolearner",
    "display_name": "Demo Learner",
    "email": "demo@duolingo.clone",
    "password_hash": hash_password("demopassword123"),
    "role": "user",
    "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=demolearner",
    "is_active": True,
}

ADMIN_USER = {
    "id": "usr_admin",
    "username": "admin",
    "display_name": "Admin User",
    "email": "admin@duolingo.clone",
    "password_hash": hash_password("adminpassword123"),
    "role": "admin",
    "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=admin",
    "is_active": True,
}

DEMO_USER_STATS = {
    "id": "stats_demo",
    "user_id": "usr_demo",
    "total_xp": 150,
    "current_streak": 7,
    "longest_streak": 12,
    "hearts": 5,
    "gems": 450,
    "daily_goal_xp": 20,
    "daily_xp": 25,
}

LEADERBOARD_USERS = [
    {
        "id": "usr_polyglot",
        "username": "polyglotpete",
        "display_name": "Polyglot Pete",
        "email": "pete@example.com",
        "password_hash": hash_password("polyglotpete123"),
        "role": "user",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=polyglotpete",
        "xp": 340,
        "rank": 1,
    },
    {
        "id": "usr_language_lover",
        "username": "languagelover",
        "display_name": "Language Lover",
        "email": "lover@example.com",
        "password_hash": hash_password("languagelover123"),
        "role": "user",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=languagelover",
        "xp": 280,
        "rank": 2,
    },
    {
        "id": "usr_spanish_pro",
        "username": "spanishpro",
        "display_name": "Spanish Pro",
        "email": "pro@example.com",
        "password_hash": hash_password("spanishpro123"),
        "role": "user",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=spanishpro",
        "xp": 210,
        "rank": 3,
    },
]

DEMO_SKILL_PROGRESSIONS = [
    {
        "id": "prg_demo_greetings",
        "user_id": "usr_demo",
        "skill_id": "skill_greetings",
        "status": "completed",
        "completion_percent": 100.0,
        "crown_level": 1,
        "lessons_completed": 2,
        "xp_earned": 30,
    },
    {
        "id": "prg_demo_basics",
        "user_id": "usr_demo",
        "skill_id": "skill_basics",
        "status": "in_progress",
        "completion_percent": 50.0,
        "crown_level": 0,
        "lessons_completed": 1,
        "xp_earned": 20,
    },
    {
        "id": "prg_demo_food",
        "user_id": "usr_demo",
        "skill_id": "skill_food",
        "status": "available",
        "completion_percent": 0.0,
        "crown_level": 0,
        "lessons_completed": 0,
        "xp_earned": 0,
    },
]

def get_demo_daily_activities():
    today = date.today()
    return [
        {
            "id": f"act_demo_{i}",
            "user_id": "usr_demo",
            "activity_date": today - timedelta(days=i),
            "xp_earned": 25 if i == 0 else 30,
            "lessons_completed": 2,
            "minutes_learned": 10,
            "goal_completed": True,
        }
        for i in range(7)
    ]
