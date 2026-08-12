import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_leaderboard(client: AsyncClient):
    response = await client.get("/api/v1/leaderboard?league=Bronze")
    assert response.status_code == 200
    data = response.json()
    assert data["league_name"] == "Bronze"
    assert isinstance(data["entries"], list)
