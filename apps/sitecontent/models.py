"""Models for site content."""
from __future__ import annotations

from django.db import models


class ContactSubmission(models.Model):
    """Contact form submissions."""

    name = models.CharField(
        max_length=200,
        help_text="Sender's name",
    )

    email = models.EmailField(
        help_text="Sender's email",
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Sender's phone number",
    )

    subject = models.CharField(
        max_length=200,
        help_text="Message subject",
    )

    message = models.TextField(
        help_text="Message content",
    )

    is_read = models.BooleanField(
        default=False,
        help_text="Whether message has been read",
    )

    replied = models.BooleanField(
        default=False,
        help_text="Whether we have replied",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        """String representation."""
        return f"{self.name} - {self.subject}"


