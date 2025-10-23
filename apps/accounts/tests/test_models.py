"""Tests for accounts models."""
from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model

Customer = get_user_model()


@pytest.mark.django_db
class TestCustomerModel:
    """Tests for Customer model."""

    def test_create_user(self):
        """Test creating a regular user."""
        user = Customer.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        assert user.email == "test@example.com"
        assert user.first_name == "Test"
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False
        assert user.check_password("testpass123")

    def test_create_superuser(self):
        """Test creating a superuser."""
        admin = Customer.objects.create_superuser(
            email="admin@example.com",
            password="admin123",
        )
        assert admin.email == "admin@example.com"
        assert admin.is_active is True
        assert admin.is_staff is True
        assert admin.is_superuser is True
        assert admin.email_verified is True

    def test_user_str(self):
        """Test user string representation."""
        user = Customer.objects.create_user(
            email="test@example.com",
            password="testpass123",
        )
        assert str(user) == "test@example.com"

    def test_get_full_name(self):
        """Test get_full_name method."""
        user = Customer.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="John",
            last_name="Doe",
        )
        assert user.get_full_name() == "John Doe"

        # Test with no name set
        user2 = Customer.objects.create_user(
            email="test2@example.com",
            password="testpass123",
        )
        assert user2.get_full_name() == "test2@example.com"


