"""URL patterns for API endpoints."""
from __future__ import annotations

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

# Create router and register viewsets
router = DefaultRouter()
router.register(r"services", views.ServiceViewSet, basename="service")
router.register(r"staff", views.StaffViewSet, basename="staff")
router.register(r"time-slots", views.TimeSlotViewSet, basename="timeslot")
router.register(r"bookings", views.BookingViewSet, basename="booking")

urlpatterns = [
    # API root
    path("", views.api_root, name="api_root"),
    # JWT Authentication
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # User registration and profile
    path("register/", views.CustomerRegistrationView.as_view(), name="register"),
    path("profile/", views.CustomerProfileView.as_view(), name="profile"),
    # Router URLs
    path("", include(router.urls)),
]


