"""Sitemaps for SEO."""
from __future__ import annotations

from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages."""

    priority = 0.8
    changefreq = "weekly"

    def items(self):
        """Return list of static page names."""
        return ["home", "about", "contact", "services"]

    def location(self, item):
        """Return URL for item."""
        return reverse(item)


class ServiceSitemap(Sitemap):
    """Sitemap for service pages."""

    priority = 0.9
    changefreq = "weekly"

    def items(self):
        """Return list of services."""
        from apps.booking.models import Service

        return Service.objects.filter(is_active=True)

    def lastmod(self, obj):
        """Return last modified date."""
        return obj.updated_at


class StaffSitemap(Sitemap):
    """Sitemap for staff/stylist pages."""

    priority = 0.7
    changefreq = "monthly"

    def items(self):
        """Return list of staff members."""
        from apps.booking.models import Staff

        return Staff.objects.filter(is_active=True)

    def lastmod(self, obj):
        """Return last modified date."""
        return obj.updated_at


