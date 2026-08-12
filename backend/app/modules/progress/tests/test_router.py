import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_user_progress(client: AsyncClient):
    response = await client.get("/api/v1/progress/usr_01/crs_spanish")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "usr_01"
    assert data["course_id"] == "crs_spanish"
