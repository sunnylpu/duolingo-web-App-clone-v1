# Duolingo Clone Database Documentation

## Database Strategy

The Duolingo Clone uses **SQLAlchemy 2.0 ORM** as its database persistence layer. 

During **Phase 01**, the application runs on **SQLite** for rapid local development, zero-dependency testing, and minimal overhead. However, the database layer is designed from day one to support migration to **PostgreSQL** with zero changes to business logic or domain repositories.

---

## Configuration & Engine Initialization

The database connection string is managed dynamically via Pydantic Settings (`DATABASE_URL` in `app/config.py`).

- **Development / SQLite**: `DATABASE_URL=sqlite:///./data/duolingo.db`
- **Production / PostgreSQL**: `DATABASE_URL=postgresql+psycopg2://user:password@db.example.com:5432/duolingo`

---

## Shared Database Infrastructure (`app/shared/database.py`)

- `Base`: SQLAlchemy `DeclarativeBase` root class for all domain models.
- `engine`: SQLAlchemy engine instance configured with thread-safe connection pooling.
- `SessionLocal`: `sessionmaker` factory for creating scoped database sessions.
- `get_db()`: FastAPI dependency yielding a clean database session per HTTP request and guaranteeing proper session teardown upon request completion.

---

## SQLite to PostgreSQL Migration Roadmap

To transition the backend from SQLite to PostgreSQL in production:

1. **Add PostgreSQL Driver**:
   Add `psycopg2-binary` or `asyncpg` to `backend/requirements.txt`.

2. **Update Environment Variable**:
   Set `DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<dbname>` in production configuration or `.env`.

3. **Database Migrations with Alembic**:
   Initialize Alembic for schema migrations:
   ```bash
   alembic init alembic
   ```
   Point Alembic's `env.py` to `app.shared.database.Base.metadata`.

4. **Enum and JSON Types**:
   Ensure custom SQLAlchemy types leverage native PostgreSQL features (e.g. `pg.ENUM` and `pg.JSONB`) via standard SQLAlchemy dialect fallbacks.
