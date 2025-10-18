# Standard library imports
import datetime
import json
from itertools import groupby

# Third-party library imports (e.g., Django, Django REST Framework)
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from django.db.models import Q
from django.http import FileResponse, JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

# Application-specific imports (from other parts of your project)
from api_service.views import send_reservation_mail_view

# Local application imports (from the current package/app, using relative imports)
from .models import DailyPrice, Discount, Reservation, ReservationEditToken, Guest
from .serializers import DiscountSerializer, ReservationSerializer, GuestSerializer
from .utils import get_reservation_price

# Create your views here.
class ReservationViewSet(ModelViewSet):
    """
    API endpoint that allows Tags to be viewed or edited.
    """

    queryset = Reservation.objects.all().order_by("id")
    serializer_class = ReservationSerializer

class GuestViewSet(ModelViewSet):
    """
    API endpoint that allows Guest to be viewed or edited.
    """

    queryset = Guest.objects.all().order_by("id")
    serializer_class = GuestSerializer

class TokenValidationView(APIView):
    # If the token check needs to be public (e.g., accessed from the email link),
    # you can use AllowAny. If it should be secured, use IsAuthenticated.
    permission_classes = [] # AllowAny is the default if not set globally

    def get(self, request, token_uuid, format=None):
        """
        Check if the provided UUID corresponds to an existing and unused token.
        """
        try:
            token_instance = ReservationEditToken.objects.get(pk=token_uuid)
            print("token_instance",token_instance)
            if token_instance.used:
                return Response(
                    {"status": "invalid", "message": "Token has already been used."},
                    status=status.HTTP_410_GONE # 410 Gone is semantically appropriate
                )

            # Token exists and is not used. Return success and the reservation ID.
            return Response(
                {
                    "status": "valid",
                    "reservation_id": token_instance.reservation.pk
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            print("Error:", e)
            return Response(
                {"status": "invalid", "message": "Token not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        
class AvailableDatesAPIView(APIView):
    """
    API endpoint to retrieve currently booked (unavailable) date ranges.
    """

    def get(self, request, *args, **kwargs):
        # Define a reasonable date range to query, e.g., next year from today
        today = datetime.date.today()
        # Ensure 'today' is treated in the local timezone if your dates are timezone-aware
        # If your DateField is naive (no timezone info), just use datetime.date.today()
        # If it's timezone aware, use timezone.localdate()

        # Get query parameters for start and end date if provided, otherwise default
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")

        if start_date_str:
            try:
                start_date = datetime.datetime.strptime(
                    start_date_str, "%Y-%m-%d"
                ).date()
            except ValueError:
                return Response(
                    {"detail": "Invalid start_date format. Use YYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            start_date = today

        if end_date_str:
            try:
                end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
            except ValueError:
                return Response(
                    {"detail": "Invalid end_date format. Use YYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            # Default to roughly 1 year from now if no end_date is provided
            end_date = start_date + datetime.timedelta(days=365)

        # Filter reservations that are 'pending' or 'confirmed' and overlap with the query range
        # A reservation overlaps if:
        # (check_in_date <= end_date AND check_out_date >= start_date)
        # We also need to consider the status
        reservations = Reservation.objects.filter(
            Q(status="pending") | Q(status="confirmed"),
            check_in_date__lte=end_date,
            check_out_date__gte=start_date,
        ).order_by("check_in_date")

        # Format the booked ranges for Flatpickr's 'disable' option
        booked_ranges = []
        for reservation in reservations:
            # Flatpickr's range disable requires 'from' and 'to' strings
            booked_ranges.append(
                {
                    "from": reservation.check_in_date.strftime("%Y-%m-%d"),
                    "to": reservation.check_out_date.strftime("%Y-%m-%d"),
                }
            )

        return Response(booked_ranges, status=status.HTTP_200_OK)


class DiscountViewSet(ModelViewSet):
    """
    API endpoint that allows Discount to be viewed or edited.
    """

    queryset = Discount.objects.all().order_by("id")
    serializer_class = DiscountSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Filter discounts where percentage is True
        percentage_true_discounts = queryset.filter(percentage=True)
        serializer_true = self.get_serializer(percentage_true_discounts, many=True)

        # Filter discounts where percentage is False
        percentage_false_discounts = queryset.filter(percentage=False)
        serializer_false = self.get_serializer(percentage_false_discounts, many=True)

        # Create a dictionary with the two lists
        data = {
            "percentage_true": serializer_true.data,
            "percentage_false": serializer_false.data,
        }

        return Response(data, status=status.HTTP_200_OK)


class DailyPriceDataRangesView(APIView):
    def get(self, request, *args, **kwargs):
        # 1. Get all daily prices, ordered by date
        queryset = DailyPrice.objects.all().order_by("date")
        if not queryset:
            return Response([])
        grouped_prices = []
        for price, group in groupby(queryset, key=lambda x: x.price):
            group_list = list(group)

            # 3. Get the start and end dates for each group
            start_date = group_list[0].date
            end_date = group_list[-1].date

            grouped_prices.append(
                {"price": price, "start_date": start_date, "end_date": end_date}
            )

        # 4. Return the new structured data
        return Response(grouped_prices)


# Create reservation and send email
@csrf_exempt
@require_POST
def create_reservation(request):
    print("Received reservation request")
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    # 1. Validate and Create the Guest
    guest_data = {
        "name": data.get("name", ""),
        "email": data.get("mail", ""),
        "vat": "12345678P",
        "document_type": "NIF",
    }
    print("guest_data", guest_data)
    guest_serializer = GuestSerializer(data=guest_data)

    if not guest_serializer.is_valid():
        print("Guest data is INVALID!")
        print("Validation Errors:", guest_serializer.errors)
        return JsonResponse({"errors": guest_serializer.errors}, status=400)

    # If valid, save the guest
    guest = guest_serializer.save()
    print(f"Successfully created guest: {guest} with ID: {guest.id}")

    # 2. Validate and Create the Reservation using the new Guest's ID

    reservation_price = get_reservation_price(request, data)
    print("\n\n\n reservation_price", reservation_price)
    reservation_data = {
        "status": "pending",
        "check_in_date": data.get("checkInDate", ""),
        "check_out_date": data.get("checkOutDate", ""),
        "num_adults": int(data.get("n_adults", "")),
        "num_children": int(data.get("n_childs", "")),
        "total_guest": (int(data.get("n_adults", "")) + data.get("n_childs", "")),
        "main_guest": guest.id,
        "total_price": float(reservation_price["total_price"])
    }
    reservation_serializer = ReservationSerializer(data=reservation_data)

    if not reservation_serializer.is_valid():
        print("Reservation data is INVALID!")
        print("Validation Errors:", reservation_serializer.errors)
        # Important: If reservation fails, you might want to delete the guest you just created
        guest.delete()
        return JsonResponse({"errors": reservation_serializer.errors}, status=400)

    # If valid, save the reservation
    try:
        reservation = reservation_serializer.save()
        print(f"Successfully created reservation: {reservation}")

        # 3. Send confirmation email
        send_reservation_mail_view(
            request
        )  # You might want to pass reservation details here

        return JsonResponse(
            {
                "message": "Reservation created successfully!",
                "reservation_id": reservation.id,
            },
            status=201,
        )

    except Exception as e:
        # Handle any other errors during save or email sending
        print(f"Error during final save or mail sending: {e}")
        # Again, consider deleting the created guest if the process fails here
        guest.delete()
        return JsonResponse({"error": "An internal error occurred."}, status=500)

@csrf_exempt
@require_POST
def edit_reservation(request):
    print("aaaa")
    return JsonResponse(
            {
                "message": "Reservation created successfully!",
                "reservation_id": 8,
            },
            status=201,
    )

@csrf_exempt
@require_POST
def calculate_reservation_price(request):
    print("Received reservation request")
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    # 1. Validate data
    reservation_price = get_reservation_price(request, data)

    return JsonResponse(
            {               
                "base_price": str(reservation_price["base_price"]),
                "total_price": str(reservation_price["total_price"]),
                "max_reduction": str(reservation_price["max_reduction"]),
            },
            status=200,
    )