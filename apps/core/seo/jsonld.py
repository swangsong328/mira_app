"""JSON-LD structured data generators for schema.org markup."""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from django.conf import settings


def generate_jsonld(schema_type: str, data: Dict[str, Any]) -> str:
    """
    Generate JSON-LD structured data.

    Args:
        schema_type: Schema.org type (e.g., 'BeautySalon', 'Service')
        data: Data dictionary for the schema

    Returns:
        JSON-LD string for embedding in HTML
    """
    jsonld = {
        "@context": "https://schema.org",
        "@type": schema_type,
        **data,
    }
    return json.dumps(jsonld, ensure_ascii=False)


def generate_beauty_salon_jsonld(
    name: str,
    description: str,
    address: Optional[Dict[str, str]] = None,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    opening_hours: Optional[List[str]] = None,
    url: Optional[str] = None,
) -> str:
    """
    Generate BeautySalon schema.org JSON-LD.

    Args:
        name: Salon name
        description: Salon description
        address: Address dictionary with street, city, state, postalCode, country
        phone: Phone number
        email: Contact email
        opening_hours: List of opening hours (e.g., ['Mo-Fr 09:00-18:00'])
        url: Website URL

    Returns:
        JSON-LD string
    """
    data: Dict[str, Any] = {
        "name": name,
        "description": description,
    }

    if url:
        data["url"] = url

    if address:
        data["address"] = {
            "@type": "PostalAddress",
            "streetAddress": address.get("street", ""),
            "addressLocality": address.get("city", ""),
            "addressRegion": address.get("state", ""),
            "postalCode": address.get("postalCode", ""),
            "addressCountry": address.get("country", ""),
        }

    if phone:
        data["telephone"] = phone

    if email:
        data["email"] = email

    if opening_hours:
        data["openingHoursSpecification"] = [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": day.split()[0], "opens": "09:00", "closes": "18:00"}
            for day in opening_hours
        ]

    return generate_jsonld("BeautySalon", data)


def generate_service_jsonld(
    name: str,
    description: str,
    price: Optional[float] = None,
    currency: str = "USD",
    duration: Optional[str] = None,
) -> str:
    """
    Generate Service schema.org JSON-LD.

    Args:
        name: Service name
        description: Service description
        price: Service price
        currency: Price currency (ISO 4217)
        duration: Service duration in ISO 8601 format (e.g., 'PT1H30M')

    Returns:
        JSON-LD string
    """
    data: Dict[str, Any] = {
        "name": name,
        "description": description,
        "serviceType": "Beauty Service",
    }

    if price is not None:
        data["offers"] = {
            "@type": "Offer",
            "price": str(price),
            "priceCurrency": currency,
        }

    if duration:
        data["duration"] = duration

    return generate_jsonld("Service", data)


def generate_breadcrumb_jsonld(breadcrumbs: List[Dict[str, str]]) -> str:
    """
    Generate BreadcrumbList schema.org JSON-LD.

    Args:
        breadcrumbs: List of breadcrumb items with 'name' and 'url'

    Returns:
        JSON-LD string
    """
    items = [
        {
            "@type": "ListItem",
            "position": idx + 1,
            "name": item["name"],
            "item": item["url"],
        }
        for idx, item in enumerate(breadcrumbs)
    ]

    data = {
        "itemListElement": items,
    }

    return generate_jsonld("BreadcrumbList", data)


def generate_local_business_jsonld(
    name: str,
    image: Optional[str] = None,
    address: Optional[Dict[str, str]] = None,
    geo: Optional[Dict[str, float]] = None,
    phone: Optional[str] = None,
    price_range: str = "$$",
) -> str:
    """
    Generate LocalBusiness schema.org JSON-LD.

    Args:
        name: Business name
        image: Business image URL
        address: Address dictionary
        geo: Geographic coordinates {'latitude': float, 'longitude': float}
        phone: Phone number
        price_range: Price range indicator (e.g., '$$', '$$$')

    Returns:
        JSON-LD string
    """
    data: Dict[str, Any] = {
        "@type": "LocalBusiness",
        "name": name,
        "priceRange": price_range,
    }

    if image:
        data["image"] = image

    if address:
        data["address"] = {
            "@type": "PostalAddress",
            **address,
        }

    if geo:
        data["geo"] = {
            "@type": "GeoCoordinates",
            "latitude": geo["latitude"],
            "longitude": geo["longitude"],
        }

    if phone:
        data["telephone"] = phone

    return generate_jsonld("LocalBusiness", data)


