"""
SkillBridge AI — Request Timing Middleware.

Measures and logs the processing time for each request.
Adds an X-Process-Time header to responses.
"""

import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.core.logging import get_logger

logger = get_logger(__name__)


class TimingMiddleware(BaseHTTPMiddleware):
    """Middleware that measures request processing time."""

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        """Process the request and measure elapsed time."""
        start_time = time.perf_counter()

        response = await call_next(request)

        process_time_ms = (time.perf_counter() - start_time) * 1000
        response.headers["X-Process-Time"] = f"{process_time_ms:.2f}ms"

        logger.info(
            "%s %s — %d — %.2fms",
            request.method,
            request.url.path,
            response.status_code,
            process_time_ms,
        )

        return response
