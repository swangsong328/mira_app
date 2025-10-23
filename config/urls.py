"""Main URL configuration."""
from __future__ import annotations

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from apps.core.health import health_check

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Health check
    path("healthz/", health_check, name="health_check"),
    # Authentication (allauth)
    path("accounts/", include("allauth.urls")),
    # Custom account views (profile, OTP)
    path("account/", include("apps.accounts.urls")),
    # API
    path("api/v1/", include("apps.api.urls")),
    # Site content
    path("", include("apps.sitecontent.urls")),
    # Booking
    path("booking/", include("apps.booking.urls")),
    # SEO
    path("sitemap.xml", include("apps.core.seo.urls")),
    path("robots.txt", include("robots.urls")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # Debug toolbar
    if "debug_toolbar" in settings.INSTALLED_APPS:
        urlpatterns = [path("__debug__/", include("debug_toolbar.urls"))] + urlpatterns

# Custom error handlers
handler404 = "apps.sitecontent.views.custom_404"
handler500 = "apps.sitecontent.views.custom_500"


