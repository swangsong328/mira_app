"""Sitecontent app configuration."""
from __future__ import annotations

from django.apps import AppConfig


class SitecontentConfig(AppConfig):
    """Configuration for Sitecontent app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.sitecontent"
    verbose_name = "Site Content"


