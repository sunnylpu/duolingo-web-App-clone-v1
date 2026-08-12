import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session
from app.modules.course.repository import CourseRepository
from app.modules.lesson.repository import LessonRepository


@pytest.mark.asyncio
async def test_list_lessons(client: AsyncClient, db_session: Session):
    c_repo = CourseRepository(db_session)
    l_repo = LessonRepository(db_session)
    c_repo.create_or_update_course("crs_t1", "Spanish", "es", "en", "es")
    c_repo.create_or_update_unit("u1", "crs_t1", "Unit 1")
    l_repo.create_or_update_skill("sk1", "u1", "Greetings")
    l_repo.create_or_update_lesson("ls1", "sk1", "Hello Lesson")

    response = await client.get("/api/v1/lessons")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["title"] == "Hello Lesson"
