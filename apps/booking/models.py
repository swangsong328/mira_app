"""Models for booking system."""
from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Optional

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class Service(models.Model):
    """
    Beauty salon service (e.g., haircut, facial, manicure).

    Each service has a name, description, duration, and price.
    """

    name = models.CharField(
        max_length=200,
        help_text="Service name (e.g., 'Classic Haircut')",
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        help_text="URL-friendly version of name",
    )

    description = models.TextField(
        help_text="Detailed service description",
    )

    short_description = models.CharField(
        max_length=300,
        blank=True,
        help_text="Brief description for listings",
    )

    duration = models.IntegerField(
        help_text="Service duration in minutes",
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Service price",
    )

    image = models.ImageField(
        upload_to="services/",
        blank=True,
        null=True,
        help_text="Service image",
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Whether service is available for booking",
    )

    # SEO fields
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)

    # Ordering
    display_order = models.IntegerField(
        default=0,
        help_text="Order in which services are displayed",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ["display_order", "name"]

    def __str__(self) -> str:
        """String representation."""
        return self.name

    def save(self, *args, **kwargs) -> None:
        """Auto-generate slug if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        """Get URL for this service."""
        return reverse("services_detail", kwargs={"slug": self.slug})

    @property
    def duration_hours(self) -> float:
        """Return duration in hours."""
        return self.duration / 60.0


class Staff(models.Model):
    """
    Salon staff member (stylist, beautician).

    Each staff member can provide multiple services.
    """

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    slug = models.SlugField(
        max_length=200,
        unique=True,
        help_text="URL-friendly identifier",
    )

    bio = models.TextField(
        blank=True,
        help_text="Staff member biography",
    )

    avatar = models.ImageField(
        upload_to="staff/",
        blank=True,
        null=True,
        help_text="Profile photo",
    )

    services = models.ManyToManyField(
        Service,
        related_name="staff_members",
        help_text="Services this staff member can provide",
    )

    email = models.EmailField(
        blank=True,
        help_text="Staff member email",
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Staff member phone",
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Whether staff member is available for booking",
    )

    display_order = models.IntegerField(
        default=0,
        help_text="Display order on staff page",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Staff Member"
        verbose_name_plural = "Staff Members"
        ordering = ["display_order", "first_name", "last_name"]

    def __str__(self) -> str:
        """String representation."""
        return self.get_full_name()

    def save(self, *args, **kwargs) -> None:
        """Auto-generate slug if not provided."""
        if not self.slug:
            self.slug = slugify(f"{self.first_name}-{self.last_name}")
        super().save(*args, **kwargs)

    def get_full_name(self) -> str:
        """Return full name."""
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self) -> str:
        """Get URL for this staff member."""
        return reverse("staff_detail", kwargs={"slug": self.slug})


class OpeningHour(models.Model):
    """
    Salon opening hours by day of week.

    Defines when the salon is open for business.
    """

    WEEKDAY_CHOICES = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]

    weekday = models.IntegerField(
        choices=WEEKDAY_CHOICES,
        unique=True,
        help_text="Day of week",
    )

    start_time = models.TimeField(
        help_text="Opening time",
    )

    end_time = models.TimeField(
        help_text="Closing time",
    )

    is_closed = models.BooleanField(
        default=False,
        help_text="Check if salon is closed this day",
    )

    class Meta:
        verbose_name = "Opening Hour"
        verbose_name_plural = "Opening Hours"
        ordering = ["weekday"]

    def __str__(self) -> str:
        """String representation."""
        day_name = self.get_weekday_display()
        if self.is_closed:
            return f"{day_name}: Closed"
        return f"{day_name}: {self.start_time} - {self.end_time}"


class TimeSlot(models.Model):
    """
    Available time slot for booking.

    Represents a specific date/time when a staff member is available.
    """

    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        related_name="time_slots",
        help_text="Staff member for this slot",
    )

    start_time = models.DateTimeField(
        help_text="Start date and time",
    )

    end_time = models.DateTimeField(
        help_text="End date and time",
    )

    capacity = models.IntegerField(
        default=1,
        help_text="Number of bookings this slot can accommodate",
    )

    is_blocked = models.BooleanField(
        default=False,
        help_text="Whether this slot is blocked (not available)",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Time Slot"
        verbose_name_plural = "Time Slots"
        ordering = ["start_time"]
        unique_together = ["staff", "start_time"]

    def __str__(self) -> str:
        """String representation."""
        return f"{self.staff} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    def clean(self) -> None:
        """Validate time slot."""
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time")

    def is_available(self) -> bool:
        """
        Check if slot is available for booking.

        Returns:
            True if slot is available
        """
        if self.is_blocked:
            return False

        if self.start_time < timezone.now():
            return False

        # Check capacity
        confirmed_bookings = self.bookings.filter(
            status__in=["pending", "confirmed"]
        ).count()

        return confirmed_bookings < self.capacity


class Booking(models.Model):
    """
    Customer booking for a service.

    Links customer, staff, service, and time slot together.
    """

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
        ("no_show", "No Show"),
    ]

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
        help_text="Customer who made the booking",
        null=True,
        blank=True,
    )
    
    # Guest booking fields (for bookings without account)
    guest_email = models.EmailField(
        blank=True,
        help_text="Guest email address (if not logged in)",
    )
    
    guest_name = models.CharField(
        max_length=255,
        blank=True,
        help_text="Guest full name (if not logged in)",
    )
    
    guest_phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Guest phone number (optional)",
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name="bookings",
        help_text="Service being booked",
    )

    staff = models.ForeignKey(
        Staff,
        on_delete=models.PROTECT,
        related_name="bookings",
        help_text="Staff member providing service",
    )

    time_slot = models.ForeignKey(
        TimeSlot,
        on_delete=models.PROTECT,
        related_name="bookings",
        help_text="Time slot for appointment",
    )

    start_time = models.DateTimeField(
        help_text="Appointment start time",
    )

    end_time = models.DateTimeField(
        help_text="Appointment end time",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        help_text="Booking status",
    )

    notes = models.TextField(
        blank=True,
        help_text="Additional notes or special requests",
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price at time of booking",
    )

    # Confirmation
    confirmation_code = models.CharField(
        max_length=32,
        unique=True,
        help_text="Unique confirmation code",
    )

    confirmed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When booking was confirmed",
    )

    # Notifications
    reminder_sent = models.BooleanField(
        default=False,
        help_text="Whether reminder notification was sent",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        """String representation."""
        customer_info = self.get_customer_email()
        return (
            f"{customer_info} - {self.service.name} - "
            f"{self.start_time.strftime('%Y-%m-%d %H:%M')}"
        )
    
    def get_customer_email(self) -> str:
        """Get customer email (from user or guest field)."""
        if self.customer:
            return self.customer.email
        return self.guest_email
    
    def get_customer_name(self) -> str:
        """Get customer name (from user or guest field)."""
        if self.customer:
            return self.customer.get_full_name() or self.customer.email
        return self.guest_name or self.guest_email

    def save(self, *args, **kwargs) -> None:
        """Generate confirmation code and calculate end time."""
        if not self.confirmation_code:
            from apps.core.utils import generate_token

            self.confirmation_code = generate_token(16)

        if not self.end_time:
            self.end_time = self.start_time + timedelta(minutes=self.service.duration)

        if not self.price:
            self.price = self.service.price

        super().save(*args, **kwargs)

    def clean(self) -> None:
        """Validate booking."""
        # Ensure either customer or guest_email is provided
        if not self.customer and not self.guest_email:
            raise ValidationError("Either customer account or guest email must be provided")
        
        # Check if service is provided by staff
        if not self.staff.services.filter(id=self.service.id).exists():
            raise ValidationError(
                f"{self.staff.get_full_name()} does not provide {self.service.name}"
            )

        # Check for overlapping bookings
        overlapping = Booking.objects.filter(
            staff=self.staff,
            status__in=["pending", "confirmed"],
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        ).exclude(id=self.id)

        if overlapping.exists():
            raise ValidationError("This time slot is not available")

    def confirm(self) -> None:
        """Confirm the booking."""
        self.status = "confirmed"
        self.confirmed_at = timezone.now()
        self.save()

        # Send confirmation email/SMS
        self.send_confirmation_notification()

    def cancel(self) -> None:
        """Cancel the booking."""
        self.status = "canceled"
        self.save()

        # Send cancellation notification
        self.send_cancellation_notification()

    def send_confirmation_notification(self) -> bool:
        """
        Send booking confirmation via email and SMS.

        Returns:
            True if notifications sent successfully
        """
        from apps.core.adapters import get_email_adapter, get_sms_adapter

        email_adapter = get_email_adapter()
        sms_adapter = get_sms_adapter()

        context = {
            "booking": self,
            "customer": self.customer,
            "customer_name": self.get_customer_name(),
            "customer_email": self.get_customer_email(),
            "service": self.service,
            "staff": self.staff,
        }

        # Send email
        email_sent = email_adapter.send_email(
            to=[self.get_customer_email()],
            subject="Booking Confirmation",
            template_name="booking_confirmation",
            context=context,
        )

        # Send SMS if customer has phone
        sms_sent = False
        # For registered users
        if self.customer and self.customer.phone and self.customer.sms_notifications:
            message = (
                f"Booking confirmed! {self.service.name} with {self.staff.get_full_name()} "
                f"on {self.start_time.strftime('%b %d at %I:%M %p')}. "
                f"Confirmation: {self.confirmation_code}"
            )
            sms_sent = sms_adapter.send_sms(to=str(self.customer.phone), message=message)
        # For guests with phone provided
        elif self.guest_phone:
            message = (
                f"Booking confirmed! {self.service.name} with {self.staff.get_full_name()} "
                f"on {self.start_time.strftime('%b %d at %I:%M %p')}. "
                f"Confirmation: {self.confirmation_code}"
            )
            sms_sent = sms_adapter.send_sms(to=self.guest_phone, message=message)

        return email_sent or sms_sent

    def send_cancellation_notification(self) -> bool:
        """
        Send booking cancellation notification.

        Returns:
            True if notifications sent successfully
        """
        from apps.core.adapters import get_email_adapter, get_sms_adapter

        email_adapter = get_email_adapter()
        sms_adapter = get_sms_adapter()

        context = {
            "booking": self,
            "customer": self.customer,
            "customer_name": self.get_customer_name(),
            "customer_email": self.get_customer_email(),
        }

        # Send email
        email_sent = email_adapter.send_email(
            to=[self.get_customer_email()],
            subject="Booking Canceled",
            template_name="booking_cancellation",
            context=context,
        )

        # Send SMS if customer has phone
        sms_sent = False
        # For registered users
        if self.customer and self.customer.phone and self.customer.sms_notifications:
            message = (
                f"Your booking for {self.service.name} on "
                f"{self.start_time.strftime('%b %d at %I:%M %p')} has been canceled."
            )
            sms_sent = sms_adapter.send_sms(to=str(self.customer.phone), message=message)
        # For guests with phone provided
        elif self.guest_phone:
            message = (
                f"Your booking for {self.service.name} on "
                f"{self.start_time.strftime('%b %d at %I:%M %p')} has been canceled."
            )
            sms_sent = sms_adapter.send_sms(to=self.guest_phone, message=message)

        return email_sent or sms_sent

    def send_reminder(self) -> bool:
        """
        Send appointment reminder.

        Returns:
            True if reminder sent successfully
        """
        from apps.core.adapters import get_email_adapter, get_sms_adapter

        if self.reminder_sent:
            return False

        email_adapter = get_email_adapter()
        sms_adapter = get_sms_adapter()

        context = {
            "booking": self,
            "customer": self.customer,
            "customer_name": self.get_customer_name(),
            "customer_email": self.get_customer_email(),
        }

        # Send email
        email_adapter.send_email(
            to=[self.get_customer_email()],
            subject="Appointment Reminder",
            template_name="booking_reminder",
            context=context,
        )

        # Send SMS
        # For registered users
        if self.customer and self.customer.phone and self.customer.sms_notifications:
            message = (
                f"Reminder: {self.service.name} appointment tomorrow at "
                f"{self.start_time.strftime('%I:%M %p')} with {self.staff.get_full_name()}."
            )
            sms_adapter.send_sms(to=str(self.customer.phone), message=message)
        # For guests with phone provided
        elif self.guest_phone:
            message = (
                f"Reminder: {self.service.name} appointment tomorrow at "
                f"{self.start_time.strftime('%I:%M %p')} with {self.staff.get_full_name()}."
            )
            sms_adapter.send_sms(to=self.guest_phone, message=message)

        self.reminder_sent = True
        self.save()
        return True


