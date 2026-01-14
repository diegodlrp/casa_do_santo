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
from django.core.exceptions import ValidationError

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
        "vat": "",
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

# Helper function to process guest data and return or create a Guest instance
def process_guest_data(guest_data: dict):
    """
    Tries to find an existing Guest by 'vat' (document number) or creates a new one.
    Updates the existing guest's details.
    """
    # Map incoming JSON keys to Django model field names
    guest_model_data = {
        'name': guest_data.get('first_name'),
        'last_name': guest_data.get('last_name'),
        'last_name2': guest_data.get('last_name2', ''),
        'sex': guest_data.get('sex'),
        # Mapping 'document_type' and 'document_support' to 'vat'
        'document_type': guest_data.get('document_type', 'DNI').upper(),
        'vat': guest_data.get('vat'), # Assuming 'vat' holds the actual document number
        
        'birth_date': guest_data.get('birth_date'),
        'nacionality': guest_data.get('nacionality'),
        'address': guest_data.get('address'),
        'address_state': guest_data.get('address_state'),
        'country': guest_data.get('country'),
        'phone': guest_data.get('phone', ''),
        'mobile': guest_data.get('mobile', ''),
        'email': guest_data.get('email', ''),
        'adult': guest_data.get('adult', True),
    }

    # Clean up empty strings or nulls to match model null/blank constraints
    for key, value in list(guest_model_data.items()):
        if value in (None, ''):
            guest_model_data[key] = None
        
        # Convert birth_date string to Python date object
        if key == 'birth_date' and guest_model_data[key]:
             guest_model_data[key] = datetime.datetime.strptime(guest_model_data[key], '%Y-%m-%d').date()
        
        # Ensure document_type is one of the valid choices
        if key == 'document_type':
            valid_types = [choice[0] for choice in Guest.DOCUMENT_TYPES]
            if guest_model_data[key] not in valid_types:
                 guest_model_data[key] = 'DNI' # Default if invalid


    # 1. Try to find the guest by VAT number
    # Assuming VAT/document number is the unique identifier for a guest.
    vat_number = guest_model_data.get('vat')
    guest_instance = None

    if vat_number:
        try:
            # Check for existing guest
            guest_instance = Guest.objects.get(vat=vat_number)
            
            # Update fields of existing guest
            for key, value in guest_model_data.items():
                setattr(guest_instance, key, value)
            guest_instance.save()
            
        except Guest.DoesNotExist:
            # Create a new guest if not found
            guest_instance = Guest.objects.create(**guest_model_data)
        except Exception as e:
            print(f"Error processing guest with VAT {vat_number}: {e}")
            raise ValidationError(f"Error saving guest data for {vat_number}: {e}")
    else:
        # Handle case where VAT is missing (e.g., just create a new one)
        # This might need better error handling or defaulting based on your business logic.
        guest_instance = Guest.objects.create(**guest_model_data)

    return guest_instance


@csrf_exempt
@require_POST
def edit_reservation(request):
    """
    Processes the JSON payload to find and update an existing reservation and its guests.
    """
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST method is allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    # --- KEY CHANGE 1: Get the reservation_id from the payload ---
    reservation_id = data.get('reservation_id')
    if not reservation_id:
        return JsonResponse({"error": "Field 'reservation_id' is required to edit."}, status=400)

    try:
        with transaction.atomic():
            # --- KEY CHANGE 2: Fetch the existing Reservation object ---
            try:
                reservation = Reservation.objects.get(pk=reservation_id)
            except Reservation.DoesNotExist:
                return JsonResponse({"error": f"Reservation with ID {reservation_id} not found."}, status=404)

            # 1. Process all guest data (this can create new guests if they don't exist)
            guests_data = data.get('guests', [])
            if not guests_data:
                return JsonResponse({"error": "Reservation must include at least one guest."}, status=400)

            guest_instances = [process_guest_data(guest_data) for guest_data in guests_data]
            main_guest = guest_instances[0]
            other_guests = guest_instances[1:]

            # 2. Prepare and validate reservation data
            check_in_str = data.get('check_in_date')
            check_out_str = data.get('check_out_date')

            if not check_in_str or not check_out_str:
                return JsonResponse({"error": "Both check_in_date and check_out_date are required."}, status=400)
            
            check_in_date = datetime.datetime.strptime(check_in_str, '%Y-%m-%d').date()
            check_out_date = datetime.datetime.strptime(check_out_str, '%Y-%m-%d').date()

            if check_out_date <= check_in_date:
                return JsonResponse({"error": "Check-out date must be after check-in date."}, status=400)

            # --- KEY CHANGE 3: Update the fields of the fetched object ---
            reservation.main_guest = main_guest
            reservation.check_in_date = check_in_date
            reservation.check_out_date = check_out_date
            reservation.special_requests = data.get('special_requests', '')
            reservation.num_adults = sum(1 for guest in guest_instances if guest.adult)
            reservation.num_children = sum(1 for guest in guest_instances if not guest.adult)
            reservation.total_guests = len(guest_instances)
            # You can update other fields like status if needed
            # reservation.status = 'confirmed'

            # 4. Save the updated reservation to the database
            reservation.save()

            # 5. Set the M2M relationship for other guests
            reservation.other_guests.set(other_guests)

            print(f"Reservation with ID {reservation.pk} was updated successfully.")

            # 6. Return a success response for the update
            return JsonResponse(
                {
                    "message": "Reservation updated successfully!",
                    "reservation_id": reservation.pk,
                },
                status=200, # Use 200 OK for a successful update
            )

    except ValidationError as e:
        return JsonResponse({"errors": e.message_dict}, status=400)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return JsonResponse({"error": "An unexpected error occurred."}, status=500)
    
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