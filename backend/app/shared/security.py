"""
Security Abstraction Foundation & Auth Context Dependencies

Provides get_current_user dependency resolving current user context.
Currently resolves seeded demo learner ('usr_demo'), providing an abstraction 
ready for seamless migration to JWT-authenticated users in future phases.
"""

from typing import Optional, Dict, Any
from fastapi import Depends
from sqlalchemy.orm import Session
from app.shared.database import get_db
from app.modules.user.models import UserModel


def get_current_user(db: Session = Depends(get_db)) -> UserModel:
    """
    Dependency returning the current active user model.
    Phase 03 implementation resolves the seeded demo learner.
    """
    user = db.query(UserModel).filter(UserModel.id == "usr_demo").first()
    if not user:
        user = db.query(UserModel).filter(UserModel.username == "demolearner").first()

    if not user:
        # Transient fallback if unseeded
        user = UserModel(
            id="usr_demo",
            username="demolearner",
            display_name="Demo Learner",
            email="demo@duolingo.clone",
            avatar="https://api.dicebear.com/7.x/bottts/svg?seed=demolearner",
            is_active=True,
        )

    return user


class PasswordHasher:
    """Interface placeholder for password hashing and verification."""

    @staticmethod
    def hash_password(plain_password: str) -> str:
        """TODO(security): Implement Argon2 or bcrypt password hashing in Phase 04."""
        return f"hashed_placeholder_{plain_password}"

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """TODO(security): Implement secure password verification in Phase 04."""
        return hashed_password == f"hashed_placeholder_{plain_password}"


class TokenProvider:
    """Interface placeholder for JWT creation and decoding."""

    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[int] = None) -> str:
        """TODO(security): Implement JWT generation with exp claim in Phase 04."""
        return "placeholder_access_token"

    @staticmethod
    def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
        """TODO(security): Implement JWT verification in Phase 04."""
        if token == "placeholder_access_token":
            return {"sub": "usr_demo"}
        return None
