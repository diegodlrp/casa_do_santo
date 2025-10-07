# Standard library imports
import datetime
import json
from itertools import groupby

# Third-party library imports (e.g., Django, Django REST Framework)
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from django.db.models import Q
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
from .models import DailyPrice, Discount, Reservation
from .serializers import DiscountSerializer, ReservationSerializer, GuestSerializer

# Create your views here.
class ReservationViewSet(ModelViewSet):
    """
    API endpoint that allows Tags to be viewed or edited.
    """

    queryset = Reservation.objects.all().order_by("id")
    serializer_class = ReservationSerializer


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
    print("aaaaaaaaaaaaaavagrant")
    try:
        # recuperate data from json
        data = json.loads(request.body)
        print("data",data)
        name = data.get("name", "")
        vat = "12345678P"
        document_type = "NIF"
        mail = data.get("mail", "")
        message = data.get("message", "")
        check_in = data.get("checkInDate", "")
        check_out = data.get("checkOutDate", "")
        n_adults = data.get("n_adults", "")
        n_childs = data.get("n_childs", "")
        language = data.get("language", "")
        
        

        guest_data = {
            "name": name,
            "vat": vat,
            "document_type": document_type 
        }
        guest_serializer = GuestSerializer(data=guest_data)
        print("Guest Data being validated:", guest_data) # Print the data
        if guest_serializer.is_valid():
            # Data is valid, proceed with save...
            print("Guest data is valid!")
        else:
            # Data is INVALID! Print the errors.
            print("Guest data is INVALID!")
            print("Validation Errors:", guest_serializer.errors)



        if guest_serializer.is_valid():
            try:
                guest = guest_serializer.save()
                print(guest)
            except Exception as e:
                # Handle database save error, external service error, etc.
                print("Error during save or mail sending: ", e)
        else:
            print("88888")
        email_response = send_reservation_mail_view(request)
        return email_response
    except Exception as e:
        # Email sent failed
        print("Error: ",e)
        return JsonResponse({"message": "Email sent failed!"})
    