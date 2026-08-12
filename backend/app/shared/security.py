"""
Security Abstraction Foundation

Provides interface placeholders for authentication, password hashing, 
and token management to be implemented in future phases.
"""

from typing import Optional, Dict, Any


class PasswordHasher:
    """Interface placeholder for password hashing and verification."""

    @staticmethod
    def hash_password(plain_password: str) -> str:
        """TODO(security): Implement Argon2 or bcrypt password hashing in Phase 02."""
        return f"hashed_placeholder_{plain_password}"

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """TODO(security): Implement secure password verification in Phase 02."""
        return hashed_password == f"hashed_placeholder_{plain_password}"


class TokenProvider:
    """Interface placeholder for JWT creation and decoding."""

    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[int] = None) -> str:
        """TODO(security): Implement JWT generation with exp claim in Phase 02."""
        return "placeholder_access_token"

    @staticmethod
    def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
        """TODO(security): Implement JWT verification in Phase 02."""
        if token == "placeholder_access_token":
            return {"sub": "placeholder_user_id"}
        return None


def get_current_user_placeholder() -> Dict[str, Any]:
    """
    Placeholder dependency for resolving authenticated current user context.
    """
    return {
        "id": "placeholder-user-id",
        "username": "guest_user",
        "is_authenticated": False,
    }
