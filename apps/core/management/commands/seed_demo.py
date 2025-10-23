"""Management command to seed demo data."""
from __future__ import annotations

from datetime import datetime, time, timedelta
from decimal import Decimal

from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.accounts.models import Customer
from apps.booking.models import Booking, OpeningHour, Service, Staff, TimeSlot


class Command(BaseCommand):
    """Seed demo data for development and testing."""

    help = "Seed demo data including services, staff, opening hours, and time slots"

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before seeding",
        )

    def handle(self, *args, **options):
        """Execute command."""
        if options["clear"]:
            self.stdout.write("Clearing existing data...")
            Booking.objects.all().delete()
            TimeSlot.objects.all().delete()
            Staff.objects.all().delete()
            Service.objects.all().delete()
            OpeningHour.objects.all().delete()
            Customer.objects.filter(is_superuser=False).delete()

        self.stdout.write("Creating demo data...")

        # Create/update site
        site = Site.objects.get_current()
        site.domain = "localhost:8000"
        site.name = "Beauty Salon"
        site.save()

        # Create superuser if doesn't exist
        if not Customer.objects.filter(email="admin@beautysalon.com").exists():
            admin = Customer.objects.create_superuser(
                email="admin@beautysalon.com",
                password="admin123",
                first_name="Admin",
                last_name="User",
            )
            self.stdout.write(self.style.SUCCESS(f"Created superuser: {admin.email}"))

        # Create demo customer if doesn't exist
        if not Customer.objects.filter(email="customer@example.com").exists():
            customer = Customer.objects.create_user(
                email="customer@example.com",
                password="password123",
                first_name="Jane",
                last_name="Doe",
                phone="+1234567890",
                email_verified=True,
            )
            self.stdout.write(self.style.SUCCESS(f"Created customer: {customer.email}"))

        # Create services
        services_data = [
            {
                "name": "Classic Haircut",
                "description": "Professional haircut tailored to your style. Includes wash, cut, and blow dry.",
                "short_description": "Professional haircut with wash and style",
                "duration": 45,
                "price": Decimal("50.00"),
                "display_order": 1,
            },
            {
                "name": "Hair Coloring",
                "description": "Full hair coloring service using premium products. Includes consultation, application, and styling.",
                "short_description": "Professional hair coloring service",
                "duration": 120,
                "price": Decimal("120.00"),
                "display_order": 2,
            },
            {
                "name": "Facial Treatment",
                "description": "Relaxing facial treatment including cleansing, exfoliation, mask, and moisturizing.",
                "short_description": "Rejuvenating facial treatment",
                "duration": 60,
                "price": Decimal("80.00"),
                "display_order": 3,
            },
            {
                "name": "Manicure",
                "description": "Complete manicure service with nail shaping, cuticle care, and polish.",
                "short_description": "Professional manicure service",
                "duration": 30,
                "price": Decimal("35.00"),
                "display_order": 4,
            },
            {
                "name": "Pedicure",
                "description": "Relaxing pedicure with foot soak, exfoliation, massage, and polish.",
                "short_description": "Luxurious pedicure service",
                "duration": 45,
                "price": Decimal("50.00"),
                "display_order": 5,
            },
            {
                "name": "Makeup Application",
                "description": "Professional makeup application for any occasion.",
                "short_description": "Expert makeup application",
                "duration": 60,
                "price": Decimal("70.00"),
                "display_order": 6,
            },
        ]

        services = {}
        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                name=service_data["name"],
                defaults=service_data,
            )
            services[service.name] = service
            status = "Created" if created else "Already exists"
            self.stdout.write(f"  {status}: {service.name}")

        # Create staff
        staff_data = [
            {
                "first_name": "Sarah",
                "last_name": "Johnson",
                "bio": "Senior stylist with 10+ years of experience specializing in cuts and color.",
                "service_names": ["Classic Haircut", "Hair Coloring"],
            },
            {
                "first_name": "Emily",
                "last_name": "Chen",
                "bio": "Expert esthetician specializing in facial treatments and skincare.",
                "service_names": ["Facial Treatment", "Makeup Application"],
            },
            {
                "first_name": "Maria",
                "last_name": "Garcia",
                "bio": "Nail specialist providing beautiful manicures and pedicures.",
                "service_names": ["Manicure", "Pedicure"],
            },
            {
                "first_name": "Lisa",
                "last_name": "Anderson",
                "bio": "Versatile beauty professional offering a range of services.",
                "service_names": ["Classic Haircut", "Makeup Application", "Manicure"],
            },
        ]

        staff_members = {}
        for staff_info in staff_data:
            service_names = staff_info.pop("service_names")
            full_name = f"{staff_info['first_name']} {staff_info['last_name']}"

            staff, created = Staff.objects.get_or_create(
                first_name=staff_info["first_name"],
                last_name=staff_info["last_name"],
                defaults=staff_info,
            )

            # Add services
            for service_name in service_names:
                if service_name in services:
                    staff.services.add(services[service_name])

            staff_members[full_name] = staff
            status = "Created" if created else "Already exists"
            self.stdout.write(f"  {status}: {full_name}")

        # Create opening hours
        opening_hours_data = [
            {"weekday": 0, "start_time": time(9, 0), "end_time": time(18, 0)},  # Monday
            {"weekday": 1, "start_time": time(9, 0), "end_time": time(18, 0)},  # Tuesday
            {"weekday": 2, "start_time": time(9, 0), "end_time": time(18, 0)},  # Wednesday
            {"weekday": 3, "start_time": time(9, 0), "end_time": time(20, 0)},  # Thursday
            {"weekday": 4, "start_time": time(9, 0), "end_time": time(20, 0)},  # Friday
            {"weekday": 5, "start_time": time(9, 0), "end_time": time(17, 0)},  # Saturday
            {"weekday": 6, "is_closed": True},  # Sunday
        ]

        for hour_data in opening_hours_data:
            hour, created = OpeningHour.objects.get_or_create(
                weekday=hour_data["weekday"],
                defaults=hour_data,
            )
            status = "Created" if created else "Already exists"
            day_name = hour.get_weekday_display()
            self.stdout.write(f"  {status}: {day_name}")

        # Create time slots for next 14 days
        self.stdout.write("Creating time slots...")
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=14)
        slots_created = 0

        for staff_member in Staff.objects.filter(is_active=True):
            current_date = start_date

            while current_date <= end_date:
                weekday = current_date.weekday()

                # Check if salon is open this day
                try:
                    opening_hour = OpeningHour.objects.get(weekday=weekday)
                    if opening_hour.is_closed:
                        current_date += timedelta(days=1)
                        continue
                except OpeningHour.DoesNotExist:
                    current_date += timedelta(days=1)
                    continue

                # Create hourly slots
                current_time = datetime.combine(current_date, opening_hour.start_time)
                end_time_dt = datetime.combine(current_date, opening_hour.end_time)

                # Make timezone aware
                current_time = timezone.make_aware(current_time)
                end_time_dt = timezone.make_aware(end_time_dt)

                while current_time < end_time_dt:
                    slot_end = current_time + timedelta(hours=1)

                    # Create slot if it doesn't exist
                    slot, created = TimeSlot.objects.get_or_create(
                        staff=staff_member,
                        start_time=current_time,
                        defaults={
                            "end_time": slot_end,
                            "capacity": 1,
                        },
                    )

                    if created:
                        slots_created += 1

                    current_time += timedelta(hours=1)

                current_date += timedelta(days=1)

        self.stdout.write(self.style.SUCCESS(f"Created {slots_created} time slots"))

        # Summary
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.SUCCESS("Demo data created successfully!"))
        self.stdout.write("=" * 50)
        self.stdout.write(f"Services: {Service.objects.count()}")
        self.stdout.write(f"Staff: {Staff.objects.count()}")
        self.stdout.write(f"Opening Hours: {OpeningHour.objects.count()}")
        self.stdout.write(f"Time Slots: {TimeSlot.objects.count()}")
        self.stdout.write(f"Customers: {Customer.objects.count()}")
        self.stdout.write("\nLogin credentials:")
        self.stdout.write("  Admin: admin@beautysalon.com / admin123")
        self.stdout.write("  Customer: customer@example.com / password123")


