"""Views for booking system."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Booking, Service, Staff, TimeSlot


def services_list(request: HttpRequest) -> HttpResponse:
    """Display list of all services."""
    services = Service.objects.filter(is_active=True)

    context = {
        "services": services,
        "meta": {
            "title": "Our Services",
            "description": "Browse our beauty salon services",
        },
    }
    return render(request, "booking/services_list.html", context)


def services_detail(request: HttpRequest, slug: str) -> HttpResponse:
    """Display service details."""
    service = get_object_or_404(Service, slug=slug, is_active=True)
    staff_members = service.staff_members.filter(is_active=True)

    context = {
        "service": service,
        "staff_members": staff_members,
        "meta": {
            "title": service.meta_title or service.name,
            "description": service.meta_description or service.short_description,
        },
    }
    return render(request, "booking/service_detail.html", context)


def staff_list(request: HttpRequest) -> HttpResponse:
    """Display list of all staff members."""
    staff = Staff.objects.filter(is_active=True).prefetch_related("services")

    context = {
        "staff": staff,
        "meta": {
            "title": "Our Stylists",
            "description": "Meet our professional beauty experts",
        },
    }
    return render(request, "booking/staff_list.html", context)


def staff_detail(request: HttpRequest, slug: str) -> HttpResponse:
    """Display staff member details."""
    staff = get_object_or_404(Staff, slug=slug, is_active=True)
    services = staff.services.filter(is_active=True)

    context = {
        "staff": staff,
        "services": services,
        "meta": {
            "title": staff.get_full_name(),
            "description": staff.bio[:160] if staff.bio else "",
        },
    }
    return render(request, "booking/staff_detail.html", context)


@login_required
def booking_step1_service(request: HttpRequest) -> HttpResponse:
    """Booking step 1: Select service."""
    services = Service.objects.filter(is_active=True)

    if request.method == "POST":
        service_id = request.POST.get("service_id")
        if service_id:
            # Store in session
            request.session["booking_service_id"] = service_id
            return redirect("booking_step2_staff")

    context = {
        "services": services,
        "step": 1,
    }
    return render(request, "booking/booking_step1_service.html", context)


@login_required
def booking_step2_staff(request: HttpRequest) -> HttpResponse:
    """Booking step 2: Select staff member."""
    service_id = request.session.get("booking_service_id")
    if not service_id:
        return redirect("booking_step1_service")

    service = get_object_or_404(Service, id=service_id, is_active=True)
    staff_members = service.staff_members.filter(is_active=True)

    if request.method == "POST":
        staff_id = request.POST.get("staff_id")
        if staff_id:
            request.session["booking_staff_id"] = staff_id
            return redirect("booking_step3_time")

    context = {
        "service": service,
        "staff_members": staff_members,
        "step": 2,
    }
    return render(request, "booking/booking_step2_staff.html", context)


@login_required
def booking_step3_time(request: HttpRequest) -> HttpResponse:
    """Booking step 3: Select date and time."""
    service_id = request.session.get("booking_service_id")
    staff_id = request.session.get("booking_staff_id")

    if not service_id or not staff_id:
        return redirect("booking_step1_service")

    service = get_object_or_404(Service, id=service_id)
    staff = get_object_or_404(Staff, id=staff_id)

    # Get available time slots for next 14 days
    today = timezone.now().date()
    end_date = today + timedelta(days=14)

    available_slots = TimeSlot.objects.filter(
        staff=staff,
        start_time__date__gte=today,
        start_time__date__lte=end_date,
        is_blocked=False,
    ).order_by("start_time")

    # Group by date
    slots_by_date: Dict[str, list] = {}
    for slot in available_slots:
        if slot.is_available():
            date_key = slot.start_time.date().isoformat()
            if date_key not in slots_by_date:
                slots_by_date[date_key] = []
            slots_by_date[date_key].append(slot)

    if request.method == "POST":
        slot_id = request.POST.get("slot_id")
        if slot_id:
            request.session["booking_slot_id"] = slot_id
            return redirect("booking_step4_confirm")

    context = {
        "service": service,
        "staff": staff,
        "slots_by_date": slots_by_date,
        "step": 3,
    }
    return render(request, "booking/booking_step3_time.html", context)


@login_required
def booking_step4_confirm(request: HttpRequest) -> HttpResponse:
    """Booking step 4: Confirm and create booking."""
    service_id = request.session.get("booking_service_id")
    staff_id = request.session.get("booking_staff_id")
    slot_id = request.session.get("booking_slot_id")

    if not all([service_id, staff_id, slot_id]):
        return redirect("booking_step1_service")

    service = get_object_or_404(Service, id=service_id)
    staff = get_object_or_404(Staff, id=staff_id)
    time_slot = get_object_or_404(TimeSlot, id=slot_id)

    if request.method == "POST":
        notes = request.POST.get("notes", "")

        try:
            with transaction.atomic():
                # Create booking
                booking = Booking.objects.create(
                    customer=request.user,
                    service=service,
                    staff=staff,
                    time_slot=time_slot,
                    start_time=time_slot.start_time,
                    notes=notes,
                )

                # Confirm booking
                booking.confirm()

                # Clear session
                for key in ["booking_service_id", "booking_staff_id", "booking_slot_id"]:
                    request.session.pop(key, None)

                messages.success(
                    request,
                    f"Booking confirmed! Confirmation code: {booking.confirmation_code}",
                )
                return redirect("booking_success", confirmation_code=booking.confirmation_code)

        except Exception as e:
            messages.error(request, f"Failed to create booking: {e}")

    context = {
        "service": service,
        "staff": staff,
        "time_slot": time_slot,
        "step": 4,
    }
    return render(request, "booking/booking_step4_confirm.html", context)


@login_required
def booking_success(request: HttpRequest, confirmation_code: str) -> HttpResponse:
    """Display booking success page."""
    booking = get_object_or_404(
        Booking,
        confirmation_code=confirmation_code,
        customer=request.user,
    )

    context = {
        "booking": booking,
    }
    return render(request, "booking/booking_success.html", context)


@login_required
def my_bookings(request: HttpRequest) -> HttpResponse:
    """Display user's bookings."""
    bookings = Booking.objects.filter(customer=request.user).order_by("-start_time")

    context = {
        "bookings": bookings,
    }
    return render(request, "booking/my_bookings.html", context)


@login_required
def cancel_booking(request: HttpRequest, confirmation_code: str) -> HttpResponse:
    """Cancel a booking."""
    booking = get_object_or_404(
        Booking,
        confirmation_code=confirmation_code,
        customer=request.user,
    )

    if request.method == "POST":
        if booking.status in ["pending", "confirmed"]:
            booking.cancel()
            messages.success(request, "Booking canceled successfully.")
        else:
            messages.error(request, "This booking cannot be canceled.")

        return redirect("my_bookings")

    context = {
        "booking": booking,
    }
    return render(request, "booking/cancel_booking.html", context)


