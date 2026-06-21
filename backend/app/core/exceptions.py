"""
SkillBridge AI — Custom Exception Classes.

Provides a hierarchy of application-specific exceptions that map
to appropriate HTTP status codes and structured error responses.
"""

from typing import Any


class AppException(Exception):
    """Base application exception.

    All custom exceptions should inherit from this class to ensure
    consistent error handling across the application.
    """

    def __init__(
        self,
        message: str = "An unexpected error occurred",
        status_code: int = 500,
        detail: Any = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.detail = detail
        super().__init__(self.message)


class NotFoundError(AppException):
    """Raised when a requested resource is not found."""

    def __init__(
        self,
        message: str = "Resource not found",
        detail: Any = None,
    ) -> None:
        super().__init__(message=message, status_code=404, detail=detail)


class ValidationError(AppException):
    """Raised when input validation fails."""

    def __init__(
        self,
        message: str = "Validation error",
        detail: Any = None,
    ) -> None:
        super().__init__(message=message, status_code=422, detail=detail)


class AuthenticationError(AppException):
    """Raised when authentication fails."""

    def __init__(
        self,
        message: str = "Authentication failed",
        detail: Any = None,
    ) -> None:
        super().__init__(message=message, status_code=401, detail=detail)


class AuthorizationError(AppException):
    """Raised when a user lacks required permissions."""

    def __init__(
        self,
        message: str = "Insufficient permissions",
        detail: Any = None,
    ) -> None:
        super().__init__(message=message, status_code=403, detail=detail)


class ConflictError(AppException):
    """Raised when a resource conflict occurs (e.g., duplicate entry)."""

    def __init__(
        self,
        message: str = "Resource conflict",
        detail: Any = None,
    ) -> None:
        super().__init__(message=message, status_code=409, detail=detail)


class ServiceUnavailableError(AppException):
    """Raised when an external service is unavailable."""

    def __init__(
        self,
        message: str = "Service temporarily unavailable",
        detail: Any = None,
    ) -> None:
        super().__init__(message=message, status_code=503, detail=detail)
