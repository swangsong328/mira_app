"""Booking app configuration."""
from __future__ import annotations

from django.apps import AppConfig


class BookingConfig(AppConfig):
    """Configuration for Booking app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.booking"
    verbose_name = "Booking"


