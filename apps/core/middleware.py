"""Custom middleware for logging and monitoring."""
from __future__ import annotations

import logging
import time
from typing import Callable

from django.http import HttpRequest, HttpResponse

logger = logging.getLogger(__name__)


class LoggingMiddleware:
    """Middleware to log request/response information."""

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        """Initialize middleware."""
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Process request and log timing."""
        start_time = time.time()

        # Log request
        logger.info(
            f"Request started: {request.method} {request.path}",
            extra={
                "method": request.method,
                "path": request.path,
                "user": getattr(request.user, "id", None),
            },
        )

        response = self.get_response(request)

        # Log response
        duration = time.time() - start_time
        logger.info(
            f"Request completed: {request.method} {request.path} "
            f"- Status: {response.status_code} - Duration: {duration:.3f}s",
            extra={
                "method": request.method,
                "path": request.path,
                "status_code": response.status_code,
                "duration": duration,
                "user": getattr(request.user, "id", None),
            },
        )

        return response


