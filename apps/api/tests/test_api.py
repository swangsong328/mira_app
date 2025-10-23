"""Tests for API endpoints."""
from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

import pytest
from django.utils import timezone
from rest_framework import status

from apps.booking.models import Booking, Service, Staff, TimeSlot


@pytest.mark.django_db
class TestServiceAPI:
    """Tests for Service API endpoints."""

    def test_list_services(self, api_client):
        """Test listing services."""
        Service.objects.create(
            name="Haircut",
            description="Test",
            duration=45,
            price=Decimal("50.00"),
        )
        Service.objects.create(
            name="Facial",
            description="Test",
            duration=60,
            price=Decimal("70.00"),
        )

        response = api_client.get("/api/v1/services/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2

    def test_get_service_detail(self, api_client):
        """Test getting service detail."""
        service = Service.objects.create(
            name="Haircut",
            description="Test description",
            duration=45,
            price=Decimal("50.00"),
        )

        response = api_client.get(f"/api/v1/services/{service.slug}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Haircut"
        assert response.data["slug"] == "haircut"


@pytest.mark.django_db
class TestStaffAPI:
    """Tests for Staff API endpoints."""

    def test_list_staff(self, api_client):
        """Test listing staff members."""
        Staff.objects.create(first_name="John", last_name="Doe")
        Staff.objects.create(first_name="Jane", last_name="Smith")

        response = api_client.get("/api/v1/staff/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2

    def test_get_staff_detail(self, api_client):
        """Test getting staff detail."""
        staff = Staff.objects.create(
            first_name="John",
            last_name="Doe",
            bio="Test bio",
        )
        service = Service.objects.create(
            name="Haircut",
            description="Test",
            duration=45,
            price=Decimal("50.00"),
        )
        staff.services.add(service)

        response = api_client.get(f"/api/v1/staff/{staff.slug}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["full_name"] == "John Doe"
        assert len(response.data["services"]) == 1


@pytest.mark.django_db
class TestBookingAPI:
    """Tests for Booking API endpoints."""

    def test_list_bookings_requires_auth(self, api_client):
        """Test that listing bookings requires authentication."""
        response = api_client.get("/api/v1/bookings/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_bookings_authenticated(self, authenticated_client, customer):
        """Test listing bookings for authenticated user."""
        service = Service.objects.create(
            name="Haircut",
            description="Test",
            duration=45,
            price=Decimal("50.00"),
        )
        staff = Staff.objects.create(first_name="John", last_name="Doe")
        staff.services.add(service)

        now = timezone.now() + timedelta(days=1)
        time_slot = TimeSlot.objects.create(
            staff=staff,
            start_time=now,
            end_time=now + timedelta(hours=1),
        )

        Booking.objects.create(
            customer=customer,
            service=service,
            staff=staff,
            time_slot=time_slot,
            start_time=time_slot.start_time,
        )

        response = authenticated_client.get("/api/v1/bookings/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1

    def test_create_booking(self, authenticated_client):
        """Test creating a booking."""
        service = Service.objects.create(
            name="Haircut",
            description="Test",
            duration=45,
            price=Decimal("50.00"),
        )
        staff = Staff.objects.create(first_name="John", last_name="Doe")
        staff.services.add(service)

        now = timezone.now() + timedelta(days=1)
        time_slot = TimeSlot.objects.create(
            staff=staff,
            start_time=now,
            end_time=now + timedelta(hours=1),
        )

        data = {
            "service": service.id,
            "staff": staff.id,
            "time_slot": time_slot.id,
            "notes": "Test booking",
        }

        response = authenticated_client.post("/api/v1/bookings/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["status"] == "confirmed"
        assert response.data["notes"] == "Test booking"


@pytest.mark.django_db
class TestAuthAPI:
    """Tests for authentication API endpoints."""

    def test_register_user(self, api_client):
        """Test user registration."""
        data = {
            "email": "newuser@example.com",
            "password": "securepass123",
            "password_confirm": "securepass123",
            "first_name": "New",
            "last_name": "User",
        }

        response = api_client.post("/api/v1/register/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert "customer" in response.data
        assert "tokens" in response.data
        assert response.data["customer"]["email"] == "newuser@example.com"

    def test_get_token(self, api_client, customer):
        """Test getting JWT token."""
        data = {
            "email": "test@example.com",
            "password": "testpass123",
        }

        response = api_client.post("/api/v1/auth/token/", data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_get_profile(self, authenticated_client, customer):
        """Test getting user profile."""
        response = authenticated_client.get("/api/v1/profile/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == customer.email


