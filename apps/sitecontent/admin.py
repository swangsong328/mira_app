"""Admin configuration for sitecontent app."""
from __future__ import annotations

from django.contrib import admin

from .models import ContactSubmission


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    """Admin interface for ContactSubmission model."""

    list_display = [
        "name",
        "email",
        "subject",
        "is_read",
        "replied",
        "created_at",
    ]

    list_filter = [
        "is_read",
        "replied",
        "created_at",
    ]

    search_fields = [
        "name",
        "email",
        "subject",
        "message",
    ]

    readonly_fields = [
        "name",
        "email",
        "phone",
        "subject",
        "message",
        "created_at",
    ]

    fieldsets = (
        (
            "Contact Information",
            {
                "fields": (
                    "name",
                    "email",
                    "phone",
                )
            },
        ),
        (
            "Message",
            {
                "fields": (
                    "subject",
                    "message",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "is_read",
                    "replied",
                    "created_at",
                )
            },
        ),
    )

    actions = ["mark_as_read", "mark_as_replied"]

    ordering = ["-created_at"]

    def mark_as_read(self, request, queryset):
        """Mark selected submissions as read."""
        count = queryset.update(is_read=True)
        self.message_user(request, f"{count} submission(s) marked as read.")

    mark_as_read.short_description = "Mark as read"

    def mark_as_replied(self, request, queryset):
        """Mark selected submissions as replied."""
        count = queryset.update(replied=True, is_read=True)
        self.message_user(request, f"{count} submission(s) marked as replied.")

    mark_as_replied.short_description = "Mark as replied"


