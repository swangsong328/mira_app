"""Forms for account management."""
from __future__ import annotations

from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import Customer


class CustomerCreationForm(UserCreationForm):
    """Form for creating new customers."""

    class Meta:
        model = Customer
        fields = ("email",)


class CustomerChangeForm(UserChangeForm):
    """Form for updating customer information."""

    class Meta:
        model = Customer
        fields = ("email", "first_name", "last_name", "phone")


class PhoneVerificationForm(forms.Form):
    """Form for phone number verification."""

    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "+1234567890"}),
    )


class OTPVerificationForm(forms.Form):
    """Form for OTP code verification."""

    otp_code = forms.CharField(
        max_length=6,
        min_length=6,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "000000",
                "pattern": "[0-9]{6}",
                "inputmode": "numeric",
            }
        ),
    )


