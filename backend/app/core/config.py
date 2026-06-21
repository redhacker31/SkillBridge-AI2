"""
SkillBridge AI — Application Configuration.

Loads all settings from environment variables using Pydantic BaseSettings.
Supports .env files and runtime overrides.
"""

from functools import lru_cache
from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # -------------------------------------------------------------------------
    # Application
    # -------------------------------------------------------------------------
    app_name: str = "SkillBridge AI"
    app_version: str = "0.1.0"
    app_env: str = "development"
    debug: bool = True
    log_level: str = "INFO"

    # -------------------------------------------------------------------------
    # Backend Server
    # -------------------------------------------------------------------------
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000

    # -------------------------------------------------------------------------
    # Database
    # -------------------------------------------------------------------------
    database_url: str = (
        "postgresql+asyncpg://skillbridge:skillbridge_secret_change_me"
        "@localhost:5432/skillbridge_db"
    )
    postgres_user: str = "skillbridge"
    postgres_password: str = "skillbridge_secret_change_me"
    postgres_db: str = "skillbridge_db"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    # -------------------------------------------------------------------------
    # Security
    # -------------------------------------------------------------------------
    secret_key: str = "super-secret-key-change-me-in-production"
    jwt_secret: str = "jwt-secret-key-change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # -------------------------------------------------------------------------
    # CORS
    # -------------------------------------------------------------------------
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins string into a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def cors_origin_list(self) -> list[str]:
        """Alias for cors_origins_list to support consistent plural/singular naming."""
        return self.cors_origins_list

    @property
    def is_production(self) -> bool:
        """Check if the application is running in production."""
        return self.app_env == "production"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get cached application settings singleton."""
    return Settings()
