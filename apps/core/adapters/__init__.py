"""Communication adapters for email and SMS."""
from __future__ import annotations

from .email import EmailAdapter, get_email_adapter
from .sms import SMSAdapter, get_sms_adapter

__all__ = ["EmailAdapter", "get_email_adapter", "SMSAdapter", "get_sms_adapter"]


