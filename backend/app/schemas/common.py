"""
SkillBridge AI — Common Response Schemas.

Standardized response envelopes used across all API endpoints.
"""

from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class HealthResponse(BaseModel):
    """Response schema for the health check endpoint."""

    status: str = Field(description="Service health status")
    version: str = Field(description="Application version")
    timestamp: datetime = Field(description="Current server timestamp")
    environment: str = Field(description="Current environment")


class VersionResponse(BaseModel):
    """Response schema for the version endpoint."""

    version: str = Field(description="Application version")
    environment: str = Field(description="Current environment")
    python_version: str = Field(description="Python runtime version")


class ErrorResponse(BaseModel):
    """Standardized error response schema."""

    error: str = Field(description="Error type")
    message: str = Field(description="Human-readable error message")
    detail: Any = Field(default=None, description="Additional error details")
    request_id: str | None = Field(default=None, description="Request correlation ID")


class SuccessResponse(BaseModel, Generic[T]):
    """Generic success response envelope."""

    success: bool = Field(default=True)
    data: T
    message: str = Field(default="Operation completed successfully")


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated list response envelope."""

    items: list[T]
    total: int = Field(description="Total number of items")
    page: int = Field(description="Current page number")
    page_size: int = Field(description="Number of items per page")
    total_pages: int = Field(description="Total number of pages")
