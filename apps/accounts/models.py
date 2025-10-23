"""Custom user model for customers."""
from __future__ import annotations

from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomerManager


class Customer(AbstractUser):
    """
    Custom user model for salon customers.

    Extends Django's AbstractUser to add phone number and verification status.
    Email is primary authentication method, phone is optional.
    """

    # Remove username requirement
    username = None  # type: ignore

    # Email as primary identifier
    email = models.EmailField(
        verbose_name="email address",
        unique=True,
        help_text="Customer's email address (used for login)",
    )

    # Phone number (optional, but recommended for booking notifications)
    phone = PhoneNumberField(
        blank=True,
        null=True,
        unique=True,
        verbose_name="phone number",
        help_text="Customer's phone number for SMS notifications",
    )

    # Verification status
    email_verified = models.BooleanField(
        default=False,
        help_text="Whether email has been verified",
    )

    phone_verified = models.BooleanField(
        default=False,
        help_text="Whether phone has been verified via OTP",
    )

    # Preferences
    sms_notifications = models.BooleanField(
        default=True,
        help_text="Receive SMS notifications for bookings",
    )

    email_notifications = models.BooleanField(
        default=True,
        help_text="Receive email notifications for bookings",
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list = []

    objects = CustomerManager()

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        """String representation."""
        return self.email

    def get_full_name(self) -> str:
        """Return full name or email if name not set."""
        full_name = super().get_full_name()
        return full_name if full_name else self.email

    def send_verification_email(self) -> bool:
        """
        Send email verification link.

        Returns:
            True if email sent successfully
        """
        from apps.core.adapters import get_email_adapter

        adapter = get_email_adapter()
        # Generate verification token (handled by django-allauth)
        return adapter.send_email(
            to=[self.email],
            subject="Verify your email",
            template_name="verification_email",
            context={
                "user": self,
                "site_name": "Beauty Salon",
            },
        )

    def send_otp_sms(self, otp_code: str) -> bool:
        """
        Send OTP code via SMS.

        Args:
            otp_code: 6-digit OTP code

        Returns:
            True if SMS sent successfully
        """
        from apps.core.adapters import get_sms_adapter

        if not self.phone:
            return False

        adapter = get_sms_adapter()
        message = f"Your verification code is: {otp_code}\n\nThis code expires in 10 minutes."
        return adapter.send_sms(to=str(self.phone), message=message)


class PhoneVerification(models.Model):
    """
    Phone number verification via OTP.

    Stores temporary OTP codes for phone verification.
    """

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="phone_verifications",
    )

    phone = PhoneNumberField(
        verbose_name="phone number",
        help_text="Phone number to verify",
    )

    otp_code = models.CharField(
        max_length=6,
        help_text="6-digit OTP code",
    )

    is_verified = models.BooleanField(
        default=False,
        help_text="Whether this OTP has been successfully verified",
    )

    attempts = models.IntegerField(
        default=0,
        help_text="Number of verification attempts",
    )

    expires_at = models.DateTimeField(
        help_text="When this OTP expires",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Phone Verification"
        verbose_name_plural = "Phone Verifications"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        """String representation."""
        return f"{self.phone} - {self.otp_code}"

    def is_valid(self) -> bool:
        """
        Check if OTP is still valid.

        Returns:
            True if OTP is valid and not expired
        """
        from django.utils import timezone

        return (
            not self.is_verified
            and self.attempts < 3
            and self.expires_at > timezone.now()
        )

    def verify(self, code: str) -> bool:
        """
        Verify OTP code.

        Args:
            code: OTP code to verify

        Returns:
            True if verification successful
        """
        self.attempts += 1
        self.save()

        if self.is_valid() and self.otp_code == code:
            self.is_verified = True
            self.customer.phone_verified = True
            self.customer.save()
            self.save()
            return True

        return False

