"""Views for booking system."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
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
    slots_by_date: Dict[str, list[TimeSlot]] = {}
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


# ========================================
# GUEST BOOKING FLOW (NO LOGIN REQUIRED)
# ========================================

def guest_booking_step1_service(request: HttpRequest) -> HttpResponse:
    """
    Guest booking step 1: Select service.
    No login required.
    """
    services = Service.objects.filter(is_active=True)

    if request.method == "POST":
        service_id = request.POST.get("service_id")
        if service_id:
            # Store in session
            request.session["guest_booking_service_id"] = service_id
            return redirect("guest_booking_step2_staff")

    context = {
        "services": services,
        "step": 1,
    }
    return render(request, "booking/guest_booking_step1_service.html", context)


def guest_booking_step2_staff(request: HttpRequest) -> HttpResponse:
    """
    Guest booking step 2: Select staff member (optional - can choose "any available").
    No login required.
    """
    service_id = request.session.get("guest_booking_service_id")
    if not service_id:
        return redirect("guest_booking_step1_service")

    service = get_object_or_404(Service, id=service_id, is_active=True)
    staff_members = service.staff_members.filter(is_active=True)

    if request.method == "POST":
        staff_id = request.POST.get("staff_id")
        
        # Store staff ID or "any" for any available staff
        request.session["guest_booking_staff_id"] = staff_id if staff_id != "any" else None
        request.session["guest_booking_any_staff"] = staff_id == "any"
        return redirect("guest_booking_step3_time")

    context = {
        "service": service,
        "staff_members": staff_members,
        "step": 2,
    }
    return render(request, "booking/guest_booking_step2_staff.html", context)


def guest_booking_step3_time(request: HttpRequest) -> HttpResponse:
    """
    Guest booking step 3: Select date and time.
    No login required.
    """
    service_id = request.session.get("guest_booking_service_id")
    if not service_id:
        return redirect("guest_booking_step1_service")

    service = get_object_or_404(Service, id=service_id)
    
    # Get staff info
    any_staff = request.session.get("guest_booking_any_staff", False)
    staff_id = request.session.get("guest_booking_staff_id")
    
    # Get available time slots for next 14 days
    today = timezone.now().date()
    end_date = today + timedelta(days=14)

    if any_staff:
        # Show slots for any staff who can do this service
        available_slots = TimeSlot.objects.filter(
            staff__services=service,
            staff__is_active=True,
            start_time__date__gte=today,
            start_time__date__lte=end_date,
            is_blocked=False,
        ).select_related('staff').order_by("start_time")
        staff = None
    else:
        # Show slots for specific staff
        staff = get_object_or_404(Staff, id=staff_id) if staff_id else None
        available_slots = TimeSlot.objects.filter(
            staff=staff,
            start_time__date__gte=today,
            start_time__date__lte=end_date,
            is_blocked=False,
        ).order_by("start_time")

    # Group by date and filter available
    slots_by_date: Dict[str, list[TimeSlot]] = {}
    seen_times_for_date: Dict[str, set[datetime]] = {}
    for slot in available_slots:
        if slot.is_available():
            date_key = slot.start_time.date().isoformat()
            if date_key not in slots_by_date:
                slots_by_date[date_key] = []
            if any_staff:
                if date_key not in seen_times_for_date:
                    seen_times_for_date[date_key] = set()
                # Skip duplicate times when "Any Available" is selected so
                # guests only choose a time slot. A specific staff member will
                # be assigned automatically once the slot is booked.
                if slot.start_time in seen_times_for_date[date_key]:
                    continue
                seen_times_for_date[date_key].add(slot.start_time)
            slots_by_date[date_key].append(slot)

    if request.method == "POST":
        slot_id = request.POST.get("slot_id")
        if slot_id:
            request.session["guest_booking_slot_id"] = slot_id
            return redirect("guest_booking_step4_details")

    context = {
        "service": service,
        "staff": staff,
        "any_staff": any_staff,
        "slots_by_date": slots_by_date,
        "step": 3,
    }
    return render(request, "booking/guest_booking_step3_time.html", context)


def guest_booking_step4_details(request: HttpRequest) -> HttpResponse:
    """
    Guest booking step 4: Enter email and details, then confirm.
    No login required.
    """
    service_id = request.session.get("guest_booking_service_id")
    slot_id = request.session.get("guest_booking_slot_id")

    if not all([service_id, slot_id]):
        return redirect("guest_booking_step1_service")

    service = get_object_or_404(Service, id=service_id)
    time_slot = get_object_or_404(TimeSlot, id=slot_id)
    staff = time_slot.staff

    if request.method == "POST":
        guest_email = request.POST.get("email", "").strip()
        guest_name = request.POST.get("name", "").strip()
        guest_phone = request.POST.get("phone", "").strip()
        notes = request.POST.get("notes", "").strip()

        # Validate email
        if not guest_email:
            messages.error(request, "Email address is required.")
        else:
            try:
                validate_email(guest_email)
                
                # Create booking
                try:
                    with transaction.atomic():
                        booking = Booking.objects.create(
                            customer=None,  # No customer account
                            guest_email=guest_email,
                            guest_name=guest_name,
                            guest_phone=guest_phone,
                            service=service,
                            staff=staff,
                            time_slot=time_slot,
                            start_time=time_slot.start_time,
                            notes=notes,
                        )

                        # Confirm booking immediately
                        booking.confirm()

                        # Clear session
                        for key in [
                            "guest_booking_service_id",
                            "guest_booking_staff_id",
                            "guest_booking_any_staff",
                            "guest_booking_slot_id",
                        ]:
                            request.session.pop(key, None)

                        messages.success(
                            request,
                            f"Booking confirmed! Check your email at {guest_email} for confirmation.",
                        )
                        return redirect("guest_booking_success", confirmation_code=booking.confirmation_code)

                except Exception as e:
                    messages.error(request, f"Failed to create booking: {e}")

            except ValidationError:
                messages.error(request, "Please enter a valid email address.")

    context = {
        "service": service,
        "staff": staff,
        "time_slot": time_slot,
        "step": 4,
    }
    return render(request, "booking/guest_booking_step4_details.html", context)


def guest_booking_success(request: HttpRequest, confirmation_code: str) -> HttpResponse:
    """
    Display booking success page for guest.
    No login required.
    """
    booking = get_object_or_404(
        Booking,
        confirmation_code=confirmation_code,
    )

    context = {
        "booking": booking,
    }
    return render(request, "booking/guest_booking_success.html", context)


