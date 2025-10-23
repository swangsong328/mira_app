"""Utility functions for accounts app."""
from __future__ import annotations

import secrets
from datetime import timedelta
from typing import TYPE_CHECKING

from django.utils import timezone

if TYPE_CHECKING:
    from .models import Customer, PhoneVerification


def generate_otp_code(length: int = 6) -> str:
    """
    Generate a random OTP code.

    Args:
        length: Length of the OTP code

    Returns:
        Numeric OTP code as string
    """
    return "".join([str(secrets.randbelow(10)) for _ in range(length)])


def create_phone_verification(
    customer: Customer,
    phone: str,
    expires_in_minutes: int = 10,
) -> PhoneVerification:
    """
    Create a new phone verification entry.

    Args:
        customer: Customer instance
        phone: Phone number to verify
        expires_in_minutes: Minutes until OTP expires

    Returns:
        PhoneVerification instance
    """
    from .models import PhoneVerification

    otp_code = generate_otp_code()
    expires_at = timezone.now() + timedelta(minutes=expires_in_minutes)

    verification = PhoneVerification.objects.create(
        customer=customer,
        phone=phone,
        otp_code=otp_code,
        expires_at=expires_at,
    )

    # Send OTP via SMS
    customer.send_otp_sms(otp_code)

    return verification


def verify_phone_otp(customer: Customer, otp_code: str) -> bool:
    """
    Verify a phone OTP code.

    Args:
        customer: Customer instance
        otp_code: OTP code to verify

    Returns:
        True if verification successful
    """
    from .models import PhoneVerification

    # Get most recent unverified OTP
    verification = (
        PhoneVerification.objects.filter(
            customer=customer,
            is_verified=False,
        )
        .order_by("-created_at")
        .first()
    )

    if not verification:
        return False

    return verification.verify(otp_code)


