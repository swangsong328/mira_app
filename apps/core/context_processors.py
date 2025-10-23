"""Context processors for template rendering."""
from __future__ import annotations

from typing import Dict, Any

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest


def site_settings(request: HttpRequest) -> Dict[str, Any]:
    """
    Add site-wide settings to template context.

    Available in all templates without explicit passing.
    """
    site = get_current_site(request)

    return {
        "SITE_NAME": site.name,
        "SITE_DOMAIN": site.domain,
        "ENABLE_SEO": getattr(settings, "ENABLE_SEO_OPTIMIZATIONS", True),
    }


