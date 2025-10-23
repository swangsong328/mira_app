"""Meta tag generation for SEO."""
from __future__ import annotations

from typing import Dict, List, Optional

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest


def get_page_meta(
    request: HttpRequest,
    title: str,
    description: str,
    keywords: Optional[List[str]] = None,
    image: Optional[str] = None,
    url: Optional[str] = None,
    article: bool = False,
) -> Dict[str, str]:
    """
    Generate meta tags for a page.

    Args:
        request: HTTP request object
        title: Page title
        description: Page description
        keywords: List of keywords
        image: OG image URL
        url: Canonical URL
        article: Whether this is an article page

    Returns:
        Dictionary of meta tags for template rendering
    """
    site = get_current_site(request)
    protocol = "https" if request.is_secure() else "http"

    # Build full URLs
    base_url = f"{protocol}://{site.domain}"
    canonical_url = url or f"{base_url}{request.path}"
    og_image = image or f"{base_url}/static/images/og-default.jpg"

    meta = {
        "title": f"{title} | {site.name}",
        "description": description,
        "canonical_url": canonical_url,
        # Open Graph
        "og_title": title,
        "og_description": description,
        "og_image": og_image,
        "og_url": canonical_url,
        "og_type": "article" if article else "website",
        "og_site_name": site.name,
        # Twitter Card
        "twitter_card": "summary_large_image",
        "twitter_title": title,
        "twitter_description": description,
        "twitter_image": og_image,
    }

    if keywords:
        meta["keywords"] = ", ".join(keywords)

    return meta


