"""Template tags for SEO functionality."""
from __future__ import annotations

from typing import Dict, Any

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def jsonld(data: str) -> str:
    """
    Render JSON-LD structured data.

    Usage: {% jsonld json_data %}
    """
    return mark_safe(f'<script type="application/ld+json">{data}</script>')


@register.inclusion_tag("components/meta_tags.html", takes_context=True)
def render_meta_tags(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Render all meta tags for SEO.

    Usage: {% render_meta_tags %}
    """
    return {
        "meta": context.get("meta", {}),
    }


