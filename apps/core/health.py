"""Health check endpoint for monitoring and deployment."""
from __future__ import annotations

import logging
from typing import Any, Dict

from django.db import connection
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)


@never_cache
@require_http_methods(["GET", "HEAD"])
def health_check(request) -> JsonResponse:
    """
    Health check endpoint.

    Returns 200 if app is healthy, 503 if unhealthy.
    Checks database connectivity.
    """
    status_data: Dict[str, Any] = {
        "status": "healthy",
        "checks": {},
    }
    status_code = 200

    # Check database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        status_data["checks"]["database"] = "ok"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        status_data["checks"]["database"] = "failed"
        status_data["status"] = "unhealthy"
        status_code = 503

    return JsonResponse(status_data, status=status_code)


