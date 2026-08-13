import pytest
from datetime import date, timedelta
from httpx import AsyncClient
from sqlalchemy.orm import Session
from seed.seed import seed_database
from app.modules.progress.models import ExerciseAttemptModel, SkillProgressModel, DailyActivityModel
from app.modules.gamification.models import UserStatsModel, UserAchievementModel
from app.modules.gamification.service import GamificationService
from app.modules.leaderboard.service import LeaderboardService


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
async def test_leaderboard_periods_and_ranking(client: AsyncClient):
    # Weekly leaderboard
    res_weekly = await client.get("/api/v1/leaderboard?period=weekly")
    assert res_weekly.status_code == 200
    data_weekly = res_weekly.json()
    assert data_weekly["period"] == "weekly"
    assert "entries" in data_weekly
    assert "current_user_rank" in data_weekly
    assert data_weekly["current_user_rank"] is not None

    # Monthly leaderboard
    res_monthly = await client.get("/api/v1/leaderboard?period=monthly")
    assert res_monthly.status_code == 200
    assert res_monthly.json()["period"] == "monthly"

    # All-time leaderboard
    res_alltime = await client.get("/api/v1/leaderboard?period=all_time")
    assert res_alltime.status_code == 200
    assert res_alltime.json()["period"] == "all_time"


@pytest.mark.asyncio
async def test_leaderboard_me_endpoint(client: AsyncClient):
    response = await client.get("/api/v1/leaderboard/me?period=weekly")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "usr_demo"
    assert "rank" in data
    assert "xp" in data
    assert "total_participants" in data


@pytest.mark.asyncio
async def test_leaderboard_period_validation(client: AsyncClient):
    response = await client.get("/api/v1/leaderboard?period=yearly")
    assert response.status_code == 400
    assert "Invalid period parameter" in response.json()["error"]["message"]


@pytest.mark.asyncio
async def test_competition_ranking_ties(db_session: Session):
    service = LeaderboardService(db_session)
    res = service.get_leaderboard(period="all_time", limit=50)

    # Check structure and ranks
    assert res.total_participants >= 4
    ranks = [e.rank for e in res.entries]
    # Ranks should be monotonically increasing (or equal for ties)
    for i in range(1, len(ranks)):
        assert ranks[i] >= ranks[i - 1]
