"""
Centralized Application Configuration managed via Pydantic Settings.
Environment variables override all default values.
"""

import os
from typing import List, Union
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized Application Configuration managed via Pydantic Settings.
    Environment variables override default values.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    APP_NAME: str = Field(default="Duolingo Clone API")
    APP_ENV: str = Field(default="development")
    APP_VERSION: str = Field(default="1.0.0")
    DEBUG: bool = Field(default=True)
    DATABASE_URL: str = Field(default="sqlite:///./data/duolingo.db")
    CORS_ORIGINS: Union[str, List[str]] = Field(default="http://localhost:3000,http://127.0.0.1:3000")
    API_PREFIX: str = Field(default="/api/v1")
    APP_TIMEZONE: str = Field(default="Asia/Kolkata")

    # Security & Auth Parameters
    JWT_SECRET_KEY: str = Field(default="super_secret_duolingo_key_change_in_production_32bytes_min")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=1440)  # 24 hours
    ALLOW_DEV_AUTH_BYPASS: bool = Field(default=False)

    # JWT Claims — issuer and audience for strict validation
    JWT_ISSUER: str = Field(default="duolingo-clone-api")
    JWT_AUDIENCE: str = Field(default="duolingo-clone-web")

    # Observability & Rate Limit Parameters
    SLOW_REQUEST_THRESHOLD_MS: int = Field(default=500)

    # Heart System Configuration
    MAX_HEARTS: int = Field(default=5)
    HEART_REGEN_MINUTES: int = Field(default=30)
    PRACTICE_RECOVERY_COOLDOWN_MINUTES: int = Field(default=15)

    @model_validator(mode="after")
    def validate_production_configuration(self) -> "Settings":
        """
        Enforce fail-fast security constraints for production deployment.
        Ensures default/weak secrets or debug flags can never accidentally run in production.
        """
        if self.APP_ENV == "production":
            if (
                self.JWT_SECRET_KEY == "super_secret_duolingo_key_change_in_production_32bytes_min"
                or len(self.JWT_SECRET_KEY) < 32
            ):
                raise ValueError(
                    "FATAL: Production environment requires a strong, non-default JWT_SECRET_KEY of at least 32 characters."
                )
            if self.DEBUG:
                raise ValueError("FATAL: DEBUG mode must be disabled (False) in production environment.")
            if self.ALLOW_DEV_AUTH_BYPASS:
                raise ValueError("FATAL: ALLOW_DEV_AUTH_BYPASS cannot be enabled in production environment.")
        return self

    @property
    def cors_origins_list(self) -> List[str]:
        """Returns CORS origins as a sanitized list of origin strings."""
        if isinstance(self.CORS_ORIGINS, list):
            return self.CORS_ORIGINS
        if isinstance(self.CORS_ORIGINS, str):
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
        return ["http://localhost:3000"]


settings = Settings()
