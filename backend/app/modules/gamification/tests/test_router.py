import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session
from seed.seed import seed_database


@pytest.mark.asyncio
async def test_get_gamification_stats(client: AsyncClient, db_session: Session):
    seed_database(db_session)
    response = await client.get("/api/v1/gamification/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_xp" in data
    assert "hearts" in data
