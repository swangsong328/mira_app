"""URL patterns for accounts app."""
from __future__ import annotations

from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path("verify-phone/", views.verify_phone, name="verify_phone"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
]


