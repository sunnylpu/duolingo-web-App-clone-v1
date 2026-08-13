import pytest
from datetime import date, timedelta
from httpx import AsyncClient
from sqlalchemy.orm import Session
from seed.seed import seed_database
from app.modules.progress.models import ExerciseAttemptModel, SkillProgressModel, DailyActivityModel
from app.modules.gamification.models import UserStatsModel
from app.modules.gamification.service import GamificationService
from app.modules.progress.service import ProgressService


@pytest.fixture(autouse=True)
def setup_seed_data(db_session: Session):
    """Seed test database before API test execution."""
    seed_database(db_session)


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_get_current_user_me(client: AsyncClient):
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "usr_demo"


@pytest.mark.asyncio
async def test_get_user_stats(client: AsyncClient):
    response = await client.get("/api/v1/users/me/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_xp"] == 150
    assert data["current_streak"] == 7
    assert data["daily_goal_xp"] == 20


@pytest.mark.asyncio
async def test_learning_path_progression_states(client: AsyncClient):
    response = await client.get("/api/v1/path")
    assert response.status_code == 200
    data = response.json()
    assert "recommended_skill_id" in data
    assert data["recommended_skill_id"] is not None

    # Verify skill statuses in Unit 1 & Unit 2
    all_skills = {}
    for unit in data["units"]:
        for skill in unit["skills"]:
            all_skills[skill["id"]] = skill

    assert "skill_greetings" in all_skills
    assert all_skills["skill_greetings"]["status"] == "completed"
    assert all_skills["skill_greetings"]["completion_percent"] == 100.0

    assert "skill_basics" in all_skills
    assert all_skills["skill_basics"]["status"] in ("available", "in_progress")

    assert "skill_food" in all_skills
    assert all_skills["skill_food"]["status"] == "locked"
    assert all_skills["skill_food"]["prerequisite_title"] == "Basics"


@pytest.mark.asyncio
async def test_locked_lesson_start_access_control_rejection(client: AsyncClient):
    # Attempt to start lesson lsn_food_1 in locked skill skill_food
    response = await client.post("/api/v1/lessons/lsn_food_1/start")
    assert response.status_code == 409
    data = response.json()
    assert data["error"]["code"] == "SKILL_LOCKED"
    assert "Complete the prerequisite skill first" in data["error"]["message"]


@pytest.mark.asyncio
async def test_post_completion_unlock_cascade(client: AsyncClient, db_session: Session):
    # 1. Complete remaining lessons for skill_basics (lsn_basics_1 and lsn_basics_2)
    start1 = await client.post("/api/v1/lessons/lsn_basics_1/start")
    att1 = start1.json()["attempt_id"]
    await client.post(
        "/api/v1/lessons/lsn_basics_1/exercises/ex_bas1_1/answer",
        json={"attempt_id": att1, "answer": "bebo"},
    )
    await client.post(
        "/api/v1/lessons/lsn_basics_1/exercises/ex_bas1_2/answer",
        json={"attempt_id": att1, "answer": "Yo soy un niño"},
    )
    comp1 = await client.post("/api/v1/lessons/lsn_basics_1/complete", json={"attempt_id": att1})
    assert comp1.status_code == 200

    start2 = await client.post("/api/v1/lessons/lsn_basics_2/start")
    att2 = start2.json()["attempt_id"]
    await client.post(
        "/api/v1/lessons/lsn_basics_2/exercises/ex_bas2_1/answer",
        json={"attempt_id": att2, "answer": "Tú comes pan"},
    )
    comp2 = await client.post("/api/v1/lessons/lsn_basics_2/complete", json={"attempt_id": att2})
    assert comp2.status_code == 200

    # 2. Query path -> skill_food should now be unlocked to "available"
    path_res = await client.get("/api/v1/path")
    assert path_res.status_code == 200
    path_data = path_res.json()

    food_skill = None
    for unit in path_data["units"]:
        for skill in unit["skills"]:
            if skill["id"] == "skill_food":
                food_skill = skill

    assert food_skill is not None
    assert food_skill["status"] == "available"

    # 3. Now starting lesson in skill_food should succeed!
    food_start = await client.post("/api/v1/lessons/lsn_food_1/start")
    assert food_start.status_code == 200


@pytest.mark.asyncio
async def test_path_and_progress_single_source_sync(client: AsyncClient):
    path_res = await client.get("/api/v1/path")
    prog_res = await client.get("/api/v1/progress")

    assert path_res.status_code == 200
    assert prog_res.status_code == 200

    path_skills = {
        s["id"]: s["status"]
        for u in path_res.json()["units"]
        for s in u["skills"]
    }
    prog_skills = {
        s["skill_id"]: s["status"]
        for s in prog_res.json()["skills"]
    }

    for skill_id, status in path_skills.items():
        assert prog_skills.get(skill_id) == status
