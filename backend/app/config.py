"""
SkillBridge AI — Application Configuration

Loads settings from environment variables (.env file).
Never hardcode secrets or configuration values.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = "sqlite:///./skillbridge.db"

    # Authentication
    secret_key: str = "skillbridge-dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # File Upload
    upload_dir: str = "uploads"
    max_file_size_mb: int = 5

    # CORS
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    @property
    def cors_origin_list(self) -> list[str]:
        """Parse CORS origins string into a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def cors_origins_list(self) -> list[str]:
        """Alias for cors_origin_list to support consistent plural/singular naming."""
        return self.cors_origin_list

    @property
    def max_file_size_bytes(self) -> int:
        """Convert MB limit to bytes."""
        return self.max_file_size_mb * 1024 * 1024

    model_config = {"env_file": ".env", "extra": "ignore"}


# Singleton settings instance
settings = Settings()
