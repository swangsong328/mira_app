"""Forms for account management."""
from __future__ import annotations

from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from allauth.account.forms import SignupForm
from phonenumber_field.formfields import PhoneNumberField

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


class CustomSignupForm(SignupForm):
    """
    Custom signup form for django-allauth.
    
    Adds first_name, last_name, and optional phone number fields.
    Email verification is required before account creation.
    """
    
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'First Name',
            'autofocus': True,
        }),
        label='First Name',
    )
    
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Last Name',
        }),
        label='Last Name',
    )
    
    phone = PhoneNumberField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '+1 (123) 456-7890',
            'type': 'tel',
        }),
        label='Phone Number (Optional)',
        help_text='Optional: For SMS booking notifications',
    )
    
    def save(self, request):
        """
        Save the user with additional fields.
        Called AFTER email verification is complete.
        """
        # Call parent save method (creates user with email/password)
        user = super().save(request)
        
        # Add custom fields
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        phone = self.cleaned_data.get('phone')
        if phone:
            user.phone = phone
        
        # Mark email as verified (allauth handles this)
        user.email_verified = True
        
        user.save()
        return user


