import os
from typing import List, Union
from pydantic import Field
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
    DEBUG: bool = Field(default=True)
    DATABASE_URL: str = Field(default="sqlite:///./data/duolingo.db")
    CORS_ORIGINS: Union[str, List[str]] = Field(default="http://localhost:3000")
    API_PREFIX: str = Field(default="/api/v1")
    APP_TIMEZONE: str = Field(default="Asia/Kolkata")

    @property
    def cors_origins_list(self) -> List[str]:
        """Returns CORS origins as a sanitized list of origin strings."""
        if isinstance(self.CORS_ORIGINS, list):
            return self.CORS_ORIGINS
        if isinstance(self.CORS_ORIGINS, str):
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
        return ["http://localhost:3000"]


settings = Settings()
