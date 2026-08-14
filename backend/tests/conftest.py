import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.shared.database import Base, get_db
from app.shared.security import create_access_token

# Use in-memory SQLite database for fast, isolated testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    # Disable foreign keys temporarily during drop_all to allow clean tear down
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    session.execute(text("PRAGMA foreign_keys=ON"))
    try:
        yield session
    finally:
        session.close()
        with engine.connect() as conn:
            conn.execute(text("PRAGMA foreign_keys=OFF"))
            Base.metadata.drop_all(bind=conn)


@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    # Generate a demo-user token so all legacy tests work without needing explicit auth.
    demo_token = create_access_token("usr_demo", role="user")
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://127.0.0.1:8000",
        headers={"Authorization": f"Bearer {demo_token}", "X-Requested-With": "XMLHttpRequest"},
    ) as ac:
        yield ac
    app.dependency_overrides.clear()
