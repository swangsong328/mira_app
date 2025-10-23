"""Email adapter with pluggable backends."""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import List, Optional

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


class EmailAdapter(ABC):
    """Abstract base class for email sending."""

    @abstractmethod
    def send_email(
        self,
        to: List[str],
        subject: str,
        template_name: str,
        context: dict,
        from_email: Optional[str] = None,
        attachments: Optional[List] = None,
    ) -> bool:
        """
        Send an email using a template.

        Args:
            to: List of recipient email addresses
            subject: Email subject
            template_name: Path to email template (without extension)
            context: Template context dictionary
            from_email: Sender email (defaults to DEFAULT_FROM_EMAIL)
            attachments: List of attachments

        Returns:
            True if email sent successfully, False otherwise
        """
        pass


class DjangoEmailAdapter(EmailAdapter):
    """Django's built-in email backend adapter."""

    def send_email(
        self,
        to: List[str],
        subject: str,
        template_name: str,
        context: dict,
        from_email: Optional[str] = None,
        attachments: Optional[List] = None,
    ) -> bool:
        """Send email using Django's email backend."""
        try:
            from_email = from_email or settings.DEFAULT_FROM_EMAIL

            # Render HTML and text versions
            html_content = render_to_string(f"emails/{template_name}.html", context)
            text_content = render_to_string(f"emails/{template_name}.txt", context)

            # Create email message
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=from_email,
                to=to,
            )
            msg.attach_alternative(html_content, "text/html")

            # Add attachments if provided
            if attachments:
                for attachment in attachments:
                    msg.attach(*attachment)

            msg.send()

            logger.info(f"Email sent successfully to {to}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {to}: {e}")
            return False


class ConsoleEmailAdapter(EmailAdapter):
    """Console email adapter for development/testing."""

    def send_email(
        self,
        to: List[str],
        subject: str,
        template_name: str,
        context: dict,
        from_email: Optional[str] = None,
        attachments: Optional[List] = None,
    ) -> bool:
        """Log email to console instead of sending."""
        try:
            from_email = from_email or settings.DEFAULT_FROM_EMAIL

            # Render text version only for console
            text_content = render_to_string(f"emails/{template_name}.txt", context)

            logger.info(
                f"\n{'='*60}\n"
                f"EMAIL (Console)\n"
                f"From: {from_email}\n"
                f"To: {', '.join(to)}\n"
                f"Subject: {subject}\n"
                f"{'='*60}\n"
                f"{text_content}\n"
                f"{'='*60}\n"
            )
            return True

        except Exception as e:
            logger.error(f"Failed to log email: {e}")
            return False


def get_email_adapter() -> EmailAdapter:
    """
    Factory function to get the appropriate email adapter.

    Returns:
        Configured EmailAdapter instance
    """
    backend = settings.EMAIL_BACKEND

    if "console" in backend.lower():
        return ConsoleEmailAdapter()
    else:
        return DjangoEmailAdapter()


