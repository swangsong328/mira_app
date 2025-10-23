"""SEO-related URL patterns."""
from __future__ import annotations

from django.contrib.sitemaps.views import sitemap
from django.urls import path

from .sitemaps import ServiceSitemap, StaffSitemap, StaticViewSitemap

sitemaps = {
    "static": StaticViewSitemap,
    "services": ServiceSitemap,
    "staff": StaffSitemap,
}

urlpatterns = [
    path("", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
]


