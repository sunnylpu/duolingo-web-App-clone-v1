"""
Seed script foundation for populating initial database tables in development environments.
"""

import logging
from sqlalchemy.orm import Session
from app.shared.database import SessionLocal, Base, engine

logger = logging.getLogger("duolingo.seed")


def seed_database(db: Session) -> None:
    """Populate database with initial data (Phase 01 scaffolding)."""
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables initialized successfully.")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
