"""Serializers for API endpoints."""
from __future__ import annotations

from rest_framework import serializers

from apps.accounts.models import Customer
from apps.booking.models import Booking, Service, Staff, TimeSlot


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer model."""

    class Meta:
        model = Customer
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "email_verified",
            "phone_verified",
            "sms_notifications",
            "email_notifications",
            "created_at",
        ]
        read_only_fields = ["id", "email_verified", "phone_verified", "created_at"]


class ServiceSerializer(serializers.ModelSerializer):
    """Serializer for Service model."""

    duration_hours = serializers.ReadOnlyField()

    class Meta:
        model = Service
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "short_description",
            "duration",
            "duration_hours",
            "price",
            "image",
            "is_active",
            "display_order",
        ]


class StaffSerializer(serializers.ModelSerializer):
    """Serializer for Staff model."""

    full_name = serializers.CharField(source="get_full_name", read_only=True)
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Staff
        fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "slug",
            "bio",
            "avatar",
            "services",
            "is_active",
        ]


class StaffListSerializer(serializers.ModelSerializer):
    """Simplified serializer for staff listings."""

    full_name = serializers.CharField(source="get_full_name", read_only=True)

    class Meta:
        model = Staff
        fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "slug",
            "avatar",
        ]


class TimeSlotSerializer(serializers.ModelSerializer):
    """Serializer for TimeSlot model."""

    staff_name = serializers.CharField(source="staff.get_full_name", read_only=True)
    is_available = serializers.BooleanField(read_only=True)

    class Meta:
        model = TimeSlot
        fields = [
            "id",
            "staff",
            "staff_name",
            "start_time",
            "end_time",
            "capacity",
            "is_blocked",
            "is_available",
        ]


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model."""

    customer_email = serializers.EmailField(source="customer.email", read_only=True)
    service_name = serializers.CharField(source="service.name", read_only=True)
    staff_name = serializers.CharField(source="staff.get_full_name", read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "customer",
            "customer_email",
            "service",
            "service_name",
            "staff",
            "staff_name",
            "time_slot",
            "start_time",
            "end_time",
            "status",
            "notes",
            "price",
            "confirmation_code",
            "confirmed_at",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "confirmation_code",
            "confirmed_at",
            "created_at",
        ]


class BookingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating bookings."""

    class Meta:
        model = Booking
        fields = [
            "service",
            "staff",
            "time_slot",
            "notes",
        ]

    def validate(self, data):
        """Validate booking data."""
        service = data["service"]
        staff = data["staff"]
        time_slot = data["time_slot"]

        # Check if service is provided by staff
        if not staff.services.filter(id=service.id).exists():
            raise serializers.ValidationError(
                f"{staff.get_full_name()} does not provide {service.name}"
            )

        # Check if time slot is available
        if not time_slot.is_available():
            raise serializers.ValidationError("This time slot is not available")

        # Check if time slot belongs to the staff
        if time_slot.staff != staff:
            raise serializers.ValidationError("Time slot does not belong to selected staff")

        return data

    def create(self, validated_data):
        """Create booking with customer from request."""
        customer = self.context["request"].user
        time_slot = validated_data["time_slot"]

        booking = Booking.objects.create(
            customer=customer,
            service=validated_data["service"],
            staff=validated_data["staff"],
            time_slot=time_slot,
            start_time=time_slot.start_time,
            notes=validated_data.get("notes", ""),
        )

        # Auto-confirm booking
        booking.confirm()

        return booking


class CustomerRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for customer registration."""

    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Customer
        fields = [
            "email",
            "password",
            "password_confirm",
            "first_name",
            "last_name",
            "phone",
        ]

    def validate(self, data):
        """Validate passwords match."""
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        """Create customer with hashed password."""
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")

        customer = Customer.objects.create_user(
            **validated_data,
            password=password,
        )

        return customer


