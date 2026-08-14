import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session
from app.modules.course.repository import CourseRepository
from seed.seed import seed_database


@pytest.mark.asyncio
async def test_list_courses(client: AsyncClient, db_session: Session):
    seed_database(db_session)
    repo = CourseRepository(db_session)
    repo.create_or_update_course("crs_t1", "Spanish", "es", "en", "es", "Learn Spanish")

    response = await client.get("/api/v1/courses")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
