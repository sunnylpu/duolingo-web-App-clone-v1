"""
E2E Test Seed Script
Executable via: python3 -m seed.e2e_seed
"""

import logging
from app.shared.database import engine, Base, SessionLocal
from seed.seed import seed_database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("duolingo.seed.e2e_seed")


def seed_e2e_environment():
    logger.info("Resetting database for Playwright E2E execution...")
    Base.metadata.drop_all(bind=engine)
    db = SessionLocal()
    try:
        counts = seed_database(db)
        logger.info(f"E2E database seeded with deterministic state: {counts}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_e2e_environment()
