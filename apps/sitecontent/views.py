"""Views for site content pages."""
from __future__ import annotations

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from apps.booking.models import OpeningHour, Service, Staff
from apps.core.seo import get_page_meta

from .forms import ContactForm


def home(request: HttpRequest) -> HttpResponse:
    """
    Homepage view.

    Displays featured services and staff members.
    """
    featured_services = Service.objects.filter(is_active=True)[:3]
    featured_staff = Staff.objects.filter(is_active=True)[:4]

    meta = get_page_meta(
        request=request,
        title="Welcome to Beauty Salon",
        description="Professional beauty services including haircuts, facials, manicures, and more. Book your appointment today!",
        keywords=["beauty salon", "haircut", "facial", "manicure", "spa"],
    )

    context = {
        "featured_services": featured_services,
        "featured_staff": featured_staff,
        "meta": meta,
    }
    return render(request, "sitecontent/home.html", context)


def about(request: HttpRequest) -> HttpResponse:
    """
    About page view.

    Displays information about the salon.
    """
    staff = Staff.objects.filter(is_active=True)
    opening_hours = OpeningHour.objects.all().order_by("weekday")

    meta = get_page_meta(
        request=request,
        title="About Us",
        description="Learn about our professional beauty salon, our team, and our commitment to excellence.",
        keywords=["beauty salon", "team", "professionals"],
    )

    context = {
        "staff": staff,
        "opening_hours": opening_hours,
        "meta": meta,
    }
    return render(request, "sitecontent/about.html", context)


def contact(request: HttpRequest) -> HttpResponse:
    """
    Contact page view.

    Displays contact form and salon information.
    """
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            submission = form.save()

            # Send notification email to admin (optional)
            from apps.core.adapters import get_email_adapter

            adapter = get_email_adapter()
            adapter.send_email(
                to=["admin@beautysalon.com"],  # Configure in settings
                subject=f"New Contact Form: {submission.subject}",
                template_name="contact_notification",
                context={"submission": submission},
            )

            messages.success(
                request,
                "Thank you for contacting us! We'll get back to you soon.",
            )
            form = ContactForm()  # Reset form
    else:
        form = ContactForm()

    opening_hours = OpeningHour.objects.all().order_by("weekday")

    meta = get_page_meta(
        request=request,
        title="Contact Us",
        description="Get in touch with our beauty salon. Book an appointment or ask us any questions.",
        keywords=["contact", "beauty salon", "appointment", "location"],
    )

    context = {
        "form": form,
        "opening_hours": opening_hours,
        "meta": meta,
    }
    return render(request, "sitecontent/contact.html", context)


def custom_404(request: HttpRequest, exception=None) -> HttpResponse:
    """Custom 404 error page."""
    return render(request, "errors/404.html", status=404)


def custom_500(request: HttpRequest) -> HttpResponse:
    """Custom 500 error page."""
    return render(request, "errors/500.html", status=500)


