"""API app configuration."""
from __future__ import annotations

from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Configuration for API app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.api"
    verbose_name = "API"


