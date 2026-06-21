"""
SkillBridge AI — Request ID Middleware.

Attaches a unique X-Request-ID header to every request and response
for distributed tracing and log correlation.
"""

import uuid

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware that generates and propagates a unique request ID."""

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        """Process the request, attaching a unique ID.

        If the incoming request already has an X-Request-ID header,
        it is preserved. Otherwise, a new UUID is generated.
        """
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        # Store on request state for downstream access
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        return response
