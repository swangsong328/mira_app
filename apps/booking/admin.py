"""Admin configuration for booking app."""
from __future__ import annotations

from django.contrib import admin
from django.utils.html import format_html

from .models import Booking, OpeningHour, Service, Staff, TimeSlot


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Admin interface for Service model."""

    list_display = [
        "name",
        "duration",
        "price",
        "is_active",
        "display_order",
        "created_at",
    ]

    list_filter = [
        "is_active",
        "created_at",
    ]

    search_fields = [
        "name",
        "description",
    ]

    prepopulated_fields = {"slug": ("name",)}

    fieldsets = (
        (None, {"fields": ("name", "slug", "short_description", "description")}),
        ("Pricing & Duration", {"fields": ("price", "duration")}),
        ("Media", {"fields": ("image",)}),
        ("SEO", {"fields": ("meta_title", "meta_description", "meta_keywords")}),
        ("Settings", {"fields": ("is_active", "display_order")}),
    )

    ordering = ["display_order", "name"]


class StaffServicesInline(admin.TabularInline):
    """Inline for staff services."""

    model = Staff.services.through
    extra = 1


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    """Admin interface for Staff model."""

    list_display = [
        "get_full_name",
        "email",
        "phone",
        "is_active",
        "display_order",
    ]

    list_filter = [
        "is_active",
        "services",
    ]

    search_fields = [
        "first_name",
        "last_name",
        "email",
    ]

    prepopulated_fields = {"slug": ("first_name", "last_name")}

    filter_horizontal = ["services"]

    fieldsets = (
        (None, {"fields": ("first_name", "last_name", "slug")}),
        ("Bio & Media", {"fields": ("bio", "avatar")}),
        ("Services", {"fields": ("services",)}),
        ("Contact", {"fields": ("email", "phone")}),
        ("Settings", {"fields": ("is_active", "display_order")}),
    )

    ordering = ["display_order", "first_name"]


@admin.register(OpeningHour)
class OpeningHourAdmin(admin.ModelAdmin):
    """Admin interface for OpeningHour model."""

    list_display = [
        "get_weekday_display",
        "start_time",
        "end_time",
        "is_closed",
    ]

    list_filter = ["is_closed"]

    ordering = ["weekday"]


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    """Admin interface for TimeSlot model."""

    list_display = [
        "staff",
        "start_time",
        "end_time",
        "capacity",
        "is_blocked",
        "get_availability",
    ]

    list_filter = [
        "staff",
        "is_blocked",
        "start_time",
    ]

    search_fields = [
        "staff__first_name",
        "staff__last_name",
    ]

    date_hierarchy = "start_time"

    ordering = ["-start_time"]

    def get_availability(self, obj):
        """Show availability status."""
        if obj.is_available():
            return format_html('<span style="color: green;">✓ Available</span>')
        return format_html('<span style="color: red;">✗ Not Available</span>')

    get_availability.short_description = "Availability"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Admin interface for Booking model."""

    list_display = [
        "confirmation_code",
        "customer",
        "service",
        "staff",
        "start_time",
        "status",
        "price",
        "created_at",
    ]

    list_filter = [
        "status",
        "created_at",
        "start_time",
        "service",
        "staff",
    ]

    search_fields = [
        "customer__email",
        "customer__first_name",
        "customer__last_name",
        "confirmation_code",
    ]

    readonly_fields = [
        "confirmation_code",
        "created_at",
        "updated_at",
        "confirmed_at",
    ]

    date_hierarchy = "start_time"

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "customer",
                    "service",
                    "staff",
                    "time_slot",
                )
            },
        ),
        (
            "Appointment Details",
            {
                "fields": (
                    "start_time",
                    "end_time",
                    "price",
                    "notes",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "status",
                    "confirmation_code",
                    "confirmed_at",
                    "reminder_sent",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    actions = ["confirm_bookings", "cancel_bookings"]

    ordering = ["-created_at"]

    def confirm_bookings(self, request, queryset):
        """Admin action to confirm selected bookings."""
        count = 0
        for booking in queryset:
            if booking.status == "pending":
                booking.confirm()
                count += 1
        self.message_user(request, f"{count} booking(s) confirmed.")

    confirm_bookings.short_description = "Confirm selected bookings"

    def cancel_bookings(self, request, queryset):
        """Admin action to cancel selected bookings."""
        count = queryset.update(status="canceled")
        self.message_user(request, f"{count} booking(s) canceled.")

    cancel_bookings.short_description = "Cancel selected bookings"


