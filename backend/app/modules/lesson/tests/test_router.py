import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_lessons(client: AsyncClient):
    response = await client.get("/api/v1/lessons")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "title" in data[0]
