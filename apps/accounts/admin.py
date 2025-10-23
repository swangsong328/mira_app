"""Admin configuration for accounts app."""
from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Customer, PhoneVerification


@admin.register(Customer)
class CustomerAdmin(BaseUserAdmin):
    """Admin interface for Customer model."""

    list_display = [
        "email",
        "first_name",
        "last_name",
        "phone",
        "email_verified",
        "phone_verified",
        "is_active",
        "created_at",
    ]

    list_filter = [
        "email_verified",
        "phone_verified",
        "is_active",
        "is_staff",
        "created_at",
    ]

    search_fields = [
        "email",
        "first_name",
        "last_name",
        "phone",
    ]

    ordering = ["-created_at"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "phone")},
        ),
        (
            "Verification",
            {"fields": ("email_verified", "phone_verified")},
        ),
        (
            "Preferences",
            {"fields": ("sms_notifications", "email_notifications")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Important dates",
            {"fields": ("last_login", "date_joined")},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


@admin.register(PhoneVerification)
class PhoneVerificationAdmin(admin.ModelAdmin):
    """Admin interface for PhoneVerification model."""

    list_display = [
        "customer",
        "phone",
        "otp_code",
        "is_verified",
        "attempts",
        "expires_at",
        "created_at",
    ]

    list_filter = [
        "is_verified",
        "created_at",
    ]

    search_fields = [
        "customer__email",
        "phone",
        "otp_code",
    ]

    readonly_fields = [
        "customer",
        "phone",
        "otp_code",
        "created_at",
    ]

    ordering = ["-created_at"]


