"""Views for account management."""
from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import OTPVerificationForm, PhoneVerificationForm
from .utils import create_phone_verification, verify_phone_otp


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    """
    User profile page.

    Displays user information and verification status.
    """
    context = {
        "user": request.user,
    }
    return render(request, "account/profile.html", context)


@login_required
def verify_phone(request: HttpRequest) -> HttpResponse:
    """
    Initiate phone verification process.

    Sends OTP code to provided phone number.
    """
    if request.method == "POST":
        form = PhoneVerificationForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone"]

            # Create verification and send OTP
            create_phone_verification(request.user, phone)

            messages.success(
                request,
                "Verification code sent! Please check your phone.",
            )
            return redirect("accounts:verify_otp")
    else:
        form = PhoneVerificationForm()

    context = {"form": form}
    return render(request, "account/verify_phone.html", context)


@login_required
def verify_otp(request: HttpRequest) -> HttpResponse:
    """
    Verify OTP code.

    Validates OTP code and marks phone as verified.
    """
    if request.method == "POST":
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data["otp_code"]

            if verify_phone_otp(request.user, otp_code):
                messages.success(
                    request,
                    "Phone verified successfully!",
                )
                return redirect("accounts:profile")
            else:
                messages.error(
                    request,
                    "Invalid or expired verification code. Please try again.",
                )
    else:
        form = OTPVerificationForm()

    context = {"form": form}
    return render(request, "account/verify_otp.html", context)


