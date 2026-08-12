import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session
from app.modules.user.repository import UserRepository


@pytest.mark.asyncio
async def test_list_users(client: AsyncClient, db_session: Session):
    repo = UserRepository(db_session)
    repo.create_or_update_user("usr_t1", "user1", "User One", "u1@test.com")

    response = await client.get("/api/v1/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["email"] == "u1@test.com"
