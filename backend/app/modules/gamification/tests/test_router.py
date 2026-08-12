import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_gamification_stats(client: AsyncClient):
    response = await client.get("/api/v1/gamification/users/usr_01")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "usr_01"
    assert "xp" in data
    assert "hearts" in data
