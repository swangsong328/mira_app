"""SMS adapter with pluggable backends."""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Optional

from django.conf import settings

logger = logging.getLogger(__name__)


class SMSAdapter(ABC):
    """Abstract base class for SMS sending."""

    @abstractmethod
    def send_sms(self, to: str, message: str) -> bool:
        """
        Send an SMS message.

        Args:
            to: Recipient phone number (E.164 format recommended)
            message: SMS message content

        Returns:
            True if SMS sent successfully, False otherwise
        """
        pass


class ConsoleSMSAdapter(SMSAdapter):
    """Console SMS adapter for development/testing."""

    def send_sms(self, to: str, message: str) -> bool:
        """Log SMS to console instead of sending."""
        try:
            logger.info(
                f"\n{'='*60}\n"
                f"SMS (Console)\n"
                f"To: {to}\n"
                f"{'='*60}\n"
                f"{message}\n"
                f"{'='*60}\n"
            )
            return True
        except Exception as e:
            logger.error(f"Failed to log SMS: {e}")
            return False


class TwilioSMSAdapter(SMSAdapter):
    """Twilio SMS adapter."""

    def __init__(
        self,
        account_sid: Optional[str] = None,
        auth_token: Optional[str] = None,
        phone_number: Optional[str] = None,
    ) -> None:
        """
        Initialize Twilio adapter.

        Args:
            account_sid: Twilio account SID
            auth_token: Twilio auth token
            phone_number: Twilio phone number
        """
        self.account_sid = account_sid or settings.TWILIO_ACCOUNT_SID
        self.auth_token = auth_token or settings.TWILIO_AUTH_TOKEN
        self.phone_number = phone_number or settings.TWILIO_PHONE_NUMBER

        if not all([self.account_sid, self.auth_token, self.phone_number]):
            raise ValueError("Twilio credentials not configured")

    def send_sms(self, to: str, message: str) -> bool:
        """Send SMS using Twilio."""
        try:
            from twilio.rest import Client

            client = Client(self.account_sid, self.auth_token)

            client.messages.create(
                body=message,
                from_=self.phone_number,
                to=to,
            )

            logger.info(f"SMS sent successfully to {to}")
            return True

        except Exception as e:
            logger.error(f"Failed to send SMS to {to}: {e}")
            return False


def get_sms_adapter() -> SMSAdapter:
    """
    Factory function to get the appropriate SMS adapter.

    Returns:
        Configured SMSAdapter instance
    """
    backend = getattr(settings, "SMS_BACKEND", "console").lower()

    if backend == "twilio":
        try:
            return TwilioSMSAdapter()
        except ValueError:
            logger.warning("Twilio not configured, falling back to console")
            return ConsoleSMSAdapter()
    else:
        return ConsoleSMSAdapter()


