"""API views using Django REST Framework."""
from __future__ import annotations

from datetime import timedelta

from django.utils import timezone
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import Customer
from apps.booking.models import Booking, Service, Staff, TimeSlot

from .serializers import (
    BookingCreateSerializer,
    BookingSerializer,
    CustomerRegistrationSerializer,
    CustomerSerializer,
    ServiceSerializer,
    StaffListSerializer,
    StaffSerializer,
    TimeSlotSerializer,
)


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing and retrieving services.

    list: Get all active services
    retrieve: Get a specific service by ID or slug
    """

    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        """Filter queryset."""
        queryset = super().get_queryset()

        # Filter by staff if provided
        staff_id = self.request.query_params.get("staff_id")
        if staff_id:
            queryset = queryset.filter(staff_members__id=staff_id)

        return queryset.distinct()


class StaffViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing and retrieving staff members.

    list: Get all active staff members
    retrieve: Get a specific staff member by ID or slug
    available_slots: Get available time slots for a staff member
    """

    queryset = Staff.objects.filter(is_active=True).prefetch_related("services")
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"

    def get_serializer_class(self):
        """Use different serializer for list view."""
        if self.action == "list":
            return StaffListSerializer
        return StaffSerializer

    def get_queryset(self):
        """Filter queryset."""
        queryset = super().get_queryset()

        # Filter by service if provided
        service_id = self.request.query_params.get("service_id")
        if service_id:
            queryset = queryset.filter(services__id=service_id)

        return queryset.distinct()

    @action(detail=True, methods=["get"])
    def available_slots(self, request, slug=None):
        """Get available time slots for this staff member."""
        staff = self.get_object()

        # Get date range from query params
        days_ahead = int(request.query_params.get("days", 14))
        today = timezone.now().date()
        end_date = today + timedelta(days=days_ahead)

        # Get available slots
        slots = TimeSlot.objects.filter(
            staff=staff,
            start_time__date__gte=today,
            start_time__date__lte=end_date,
            is_blocked=False,
            start_time__gte=timezone.now(),
        ).order_by("start_time")

        # Filter only available slots
        available_slots = [slot for slot in slots if slot.is_available()]

        serializer = TimeSlotSerializer(available_slots, many=True)
        return Response(serializer.data)


class TimeSlotViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for available time slots.

    list: Get all available time slots
    retrieve: Get a specific time slot
    """

    serializer_class = TimeSlotSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Get available time slots."""
        queryset = TimeSlot.objects.filter(
            is_blocked=False,
            start_time__gte=timezone.now(),
        ).select_related("staff")

        # Filter by staff
        staff_id = self.request.query_params.get("staff_id")
        if staff_id:
            queryset = queryset.filter(staff_id=staff_id)

        # Filter by date range
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if start_date:
            queryset = queryset.filter(start_time__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(start_time__date__lte=end_date)

        return queryset.order_by("start_time")


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for bookings.

    list: Get user's bookings
    create: Create a new booking
    retrieve: Get a specific booking
    cancel: Cancel a booking
    """

    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Get bookings for current user."""
        return Booking.objects.filter(customer=self.request.user).order_by("-created_at")

    def get_serializer_class(self):
        """Use different serializer for create action."""
        if self.action == "create":
            return BookingCreateSerializer
        return BookingSerializer

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        """Cancel a booking."""
        booking = self.get_object()

        if booking.status not in ["pending", "confirmed"]:
            return Response(
                {"error": "This booking cannot be canceled"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        booking.cancel()
        serializer = self.get_serializer(booking)
        return Response(serializer.data)


class CustomerProfileView(generics.RetrieveUpdateAPIView):
    """
    Get or update customer profile.

    GET: Get current user's profile
    PUT/PATCH: Update current user's profile
    """

    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Return current user."""
        return self.request.user


class CustomerRegistrationView(generics.CreateAPIView):
    """
    Register a new customer.

    POST: Create new customer account
    """

    serializer_class = CustomerRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        """Create customer and return JWT tokens."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(customer)

        return Response(
            {
                "customer": CustomerSerializer(customer).data,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def api_root(request):
    """
    API root endpoint with available endpoints.
    """
    return Response(
        {
            "services": request.build_absolute_uri("/api/v1/services/"),
            "staff": request.build_absolute_uri("/api/v1/staff/"),
            "time_slots": request.build_absolute_uri("/api/v1/time-slots/"),
            "bookings": request.build_absolute_uri("/api/v1/bookings/"),
            "profile": request.build_absolute_uri("/api/v1/profile/"),
            "register": request.build_absolute_uri("/api/v1/register/"),
            "token": request.build_absolute_uri("/api/v1/auth/token/"),
            "token_refresh": request.build_absolute_uri("/api/v1/auth/token/refresh/"),
        }
    )


