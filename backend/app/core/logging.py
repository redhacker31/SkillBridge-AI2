"""
SkillBridge AI — Structured Logging Configuration.

Provides consistent, structured logging across the application.
Uses JSON format in production for log aggregation compatibility.
"""

import logging
import sys
from typing import Any

from app.core.config import get_settings


class StructuredFormatter(logging.Formatter):
    """Custom formatter that outputs structured log records."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with consistent structure."""
        log_data: dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if record.exc_info and record.exc_info[1]:
            log_data["exception"] = self.formatException(record.exc_info)

        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id  # type: ignore[attr-defined]

        settings = get_settings()
        if settings.is_production:
            import json

            return json.dumps(log_data)

        return (
            f"[{log_data['timestamp']}] "
            f"{log_data['level']:8s} "
            f"{log_data['logger']} — "
            f"{log_data['message']}"
        )


def setup_logging() -> None:
    """Configure application logging with structured output."""
    settings = get_settings()

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))

    # Remove any existing handlers
    root_logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(
        StructuredFormatter(datefmt="%Y-%m-%d %H:%M:%S")
    )
    root_logger.addHandler(console_handler)

    # Silence noisy third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.INFO if settings.debug else logging.WARNING
    )

    logger = logging.getLogger(__name__)
    logger.info(
        "Logging configured — level=%s, environment=%s",
        settings.log_level,
        settings.app_env,
    )


def get_logger(name: str) -> logging.Logger:
    """Get a named logger instance."""
    return logging.getLogger(name)
