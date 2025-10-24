"""URL patterns for booking app."""
from __future__ import annotations

from django.urls import path

from . import views

urlpatterns = [
    # Services
    path("services/", views.services_list, name="services"),
    path("services/<slug:slug>/", views.services_detail, name="services_detail"),
    # Staff
    path("staff/", views.staff_list, name="staff"),
    path("staff/<slug:slug>/", views.staff_detail, name="staff_detail"),
    
    # Guest Booking flow (NO LOGIN REQUIRED)
    path("book/", views.guest_booking_step1_service, name="guest_booking_step1_service"),
    path("book/step2/", views.guest_booking_step2_staff, name="guest_booking_step2_staff"),
    path("book/step3/", views.guest_booking_step3_time, name="guest_booking_step3_time"),
    path("book/step4/", views.guest_booking_step4_details, name="guest_booking_step4_details"),
    path("book/success/<str:confirmation_code>/", views.guest_booking_success, name="guest_booking_success"),
    
    # OLD Booking flow (requires login - kept for backward compatibility)
    path("new/step1/", views.booking_step1_service, name="booking_step1_service"),
    path("new/step2/", views.booking_step2_staff, name="booking_step2_staff"),
    path("new/step3/", views.booking_step3_time, name="booking_step3_time"),
    path("new/step4/", views.booking_step4_confirm, name="booking_step4_confirm"),
    path("success/<str:confirmation_code>/", views.booking_success, name="booking_success"),
    
    # My bookings
    path("my-bookings/", views.my_bookings, name="my_bookings"),
    path("cancel/<str:confirmation_code>/", views.cancel_booking, name="cancel_booking"),
]


