import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session
from seed.seed import seed_database


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
    assert data["username"] == "demolearner"
    assert "email" in data


@pytest.mark.asyncio
async def test_get_user_stats(client: AsyncClient):
    response = await client.get("/api/v1/users/me/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_xp"] == 150
    assert data["current_streak"] == 7
    assert data["hearts"] == 5


@pytest.mark.asyncio
async def test_list_courses(client: AsyncClient):
    response = await client.get("/api/v1/courses")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["code"] == "es"


@pytest.mark.asyncio
async def test_get_course_detail_and_404(client: AsyncClient):
    # Valid course
    response = await client.get("/api/v1/courses/crs_spanish")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "crs_spanish"
    assert len(data["units"]) == 3

    # Invalid course 404
    err_res = await client.get("/api/v1/courses/invalid_course_id")
    assert err_res.status_code == 404
    err_data = err_res.json()
    assert "error" in err_data
    assert err_data["error"]["code"] == "NOT_FOUND"


@pytest.mark.asyncio
async def test_get_learning_path(client: AsyncClient):
    response = await client.get("/api/v1/path")
    assert response.status_code == 200
    data = response.json()
    assert "course" in data
    assert "units" in data
    assert len(data["units"]) == 3
    # Verify skill path status
    first_skill = data["units"][0]["skills"][0]
    assert first_skill["status"] in ("locked", "available", "in_progress", "completed")


@pytest.mark.asyncio
async def test_get_lesson_detail_and_404(client: AsyncClient):
    # Valid lesson
    response = await client.get("/api/v1/lessons/lsn_greetings_1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "lsn_greetings_1"
    assert len(data["exercises"]) > 0

    # Invalid lesson 404
    err_res = await client.get("/api/v1/lessons/invalid_lesson_id")
    assert err_res.status_code == 404
    err_data = err_res.json()
    assert err_data["error"]["code"] == "NOT_FOUND"


@pytest.mark.asyncio
async def test_start_lesson_endpoint_and_reuse(client: AsyncClient):
    # Start valid lesson
    response = await client.post("/api/v1/lessons/lsn_greetings_1/start")
    assert response.status_code == 200
    data = response.json()
    assert "attempt_id" in data
    assert data["lesson_id"] == "lsn_greetings_1"
    assert data["status"] == "started"
    attempt_id_1 = data["attempt_id"]

    # Start same lesson again -> must reuse active attempt_id
    res_reuse = await client.post("/api/v1/lessons/lsn_greetings_1/start")
    assert res_reuse.status_code == 200
    data_reuse = res_reuse.json()
    assert data_reuse["attempt_id"] == attempt_id_1

    # Start invalid lesson -> returns 404
    err_res = await client.post("/api/v1/lessons/invalid_lesson_id/start")
    assert err_res.status_code == 404
    assert err_res.json()["error"]["code"] == "NOT_FOUND"


@pytest.mark.asyncio
async def test_get_user_progress(client: AsyncClient):
    response = await client.get("/api/v1/progress")
    assert response.status_code == 200
    data = response.json()
    assert "skills" in data
    assert isinstance(data["skills"], list)


@pytest.mark.asyncio
async def test_get_gamification_stats(client: AsyncClient):
    response = await client.get("/api/v1/gamification/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_xp" in data
    assert "current_streak" in data


@pytest.mark.asyncio
async def test_get_leaderboard_and_validation_error(client: AsyncClient):
    # Valid periods
    for period in ["weekly", "monthly", "all_time"]:
        res = await client.get(f"/api/v1/leaderboard?period={period}")
        assert res.status_code == 200
        data = res.json()
        assert data["period"] == period
        assert isinstance(data["entries"], list)

    # Invalid period parameter error
    err_res = await client.get("/api/v1/leaderboard?period=invalid_period")
    assert err_res.status_code == 400
    err_data = err_res.json()
    assert err_data["error"]["code"] == "VALIDATION_ERROR"


@pytest.mark.asyncio
async def test_achievements_endpoints(client: AsyncClient):
    # All achievements
    res1 = await client.get("/api/v1/achievements")
    assert res1.status_code == 200
    data1 = res1.json()
    assert len(data1) >= 4

    # User achievements
    res2 = await client.get("/api/v1/users/me/achievements")
    assert res2.status_code == 200
    data2 = res2.json()
    assert len(data2) >= 4
    assert any(a["is_earned"] for a in data2)
