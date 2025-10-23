"""Tests for booking models."""
from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.booking.models import Booking, OpeningHour, Service, Staff, TimeSlot


@pytest.mark.django_db
class TestServiceModel:
    """Tests for Service model."""

    def test_create_service(self):
        """Test creating a service."""
        service = Service.objects.create(
            name="Test Service",
            description="Test description",
            duration=60,
            price=Decimal("50.00"),
        )
        assert service.name == "Test Service"
        assert service.slug == "test-service"
        assert service.is_active is True

    def test_service_duration_hours(self):
        """Test duration_hours property."""
        service = Service.objects.create(
            name="Test Service",
            description="Test",
            duration=90,
            price=Decimal("50.00"),
        )
        assert service.duration_hours == 1.5


@pytest.mark.django_db
class TestStaffModel:
    """Tests for Staff model."""

    def test_create_staff(self):
        """Test creating a staff member."""
        staff = Staff.objects.create(
            first_name="John",
            last_name="Doe",
            bio="Test bio",
        )
        assert staff.get_full_name() == "John Doe"
        assert staff.slug == "john-doe"

    def test_staff_services(self):
        """Test staff services relationship."""
        staff = Staff.objects.create(first_name="Jane", last_name="Doe")
        service = Service.objects.create(
            name="Haircut",
            description="Test",
            duration=45,
            price=Decimal("50.00"),
        )
        staff.services.add(service)
        assert service in staff.services.all()


@pytest.mark.django_db
class TestTimeSlotModel:
    """Tests for TimeSlot model."""

    def test_create_time_slot(self):
        """Test creating a time slot."""
        staff = Staff.objects.create(first_name="John", last_name="Doe")
        now = timezone.now()
        end = now + timedelta(hours=1)

        slot = TimeSlot.objects.create(
            staff=staff,
            start_time=now,
            end_time=end,
        )
        assert slot.capacity == 1
        assert slot.is_blocked is False

    def test_time_slot_validation(self):
        """Test time slot validation."""
        staff = Staff.objects.create(first_name="John", last_name="Doe")
        now = timezone.now()

        # End time before start time should fail
        slot = TimeSlot(
            staff=staff,
            start_time=now,
            end_time=now - timedelta(hours=1),
        )
        with pytest.raises(ValidationError):
            slot.clean()


@pytest.mark.django_db
class TestBookingModel:
    """Tests for Booking model."""

    def test_create_booking(self, customer):
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

        booking = Booking.objects.create(
            customer=customer,
            service=service,
            staff=staff,
            time_slot=time_slot,
            start_time=time_slot.start_time,
        )

        assert booking.status == "pending"
        assert booking.confirmation_code is not None
        assert booking.price == service.price
        assert booking.end_time is not None

    def test_booking_validation_staff_service(self, customer):
        """Test booking validation for staff/service mismatch."""
        service = Service.objects.create(
            name="Haircut",
            description="Test",
            duration=45,
            price=Decimal("50.00"),
        )
        staff = Staff.objects.create(first_name="John", last_name="Doe")
        # Staff doesn't provide this service

        now = timezone.now() + timedelta(days=1)
        time_slot = TimeSlot.objects.create(
            staff=staff,
            start_time=now,
            end_time=now + timedelta(hours=1),
        )

        booking = Booking(
            customer=customer,
            service=service,
            staff=staff,
            time_slot=time_slot,
            start_time=time_slot.start_time,
        )

        with pytest.raises(ValidationError):
            booking.clean()


