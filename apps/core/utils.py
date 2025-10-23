"""Core utility functions."""
from __future__ import annotations

import hashlib
import secrets
from typing import Optional


def generate_token(length: int = 32) -> str:
    """
    Generate a cryptographically secure random token.

    Args:
        length: Length of the token in bytes

    Returns:
        Hexadecimal string token
    """
    return secrets.token_hex(length)


def hash_value(value: str, salt: Optional[str] = None) -> str:
    """
    Generate SHA256 hash of a value.

    Args:
        value: String to hash
        salt: Optional salt for additional security

    Returns:
        Hexadecimal hash string
    """
    data = f"{value}{salt or ''}"
    return hashlib.sha256(data.encode()).hexdigest()


