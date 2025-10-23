"""Pytest configuration and fixtures."""
from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model

Customer = get_user_model()


@pytest.fixture
def customer(db):
    """Create a test customer."""
    return Customer.objects.create_user(
        email="test@example.com",
        password="testpass123",
        first_name="Test",
        last_name="User",
    )


@pytest.fixture
def admin_customer(db):
    """Create an admin customer."""
    return Customer.objects.create_superuser(
        email="admin@example.com",
        password="admin123",
        first_name="Admin",
        last_name="User",
    )


@pytest.fixture
def api_client():
    """Create an API client."""
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def authenticated_client(customer, api_client):
    """Create an authenticated API client."""
    api_client.force_authenticate(user=customer)
    return api_client


