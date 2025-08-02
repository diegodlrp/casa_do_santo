# reservations_app/serializers.py
from rest_framework import serializers
from .models import Guest, Reservation
from django.utils.translation import gettext_lazy as _
from django.db import transaction # Needed for atomic operations in create
from django.core.mail import send_mail
import json
from django.shortcuts import render
from django.http import FileResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO
from reportlab.pdfgen import canvas

class GuestSerializer(serializers.ModelSerializer):
    """
    Serializer for the Guest model, used for nested operations within Reservation.
    """
    # Your Guest model has 'name' and 'last_name'. Your frontend sends 'first_name' and 'last_name'.
    # This maps 'first_name' from the incoming JSON to the 'name' field of the Guest model.
    first_name = serializers.CharField(source='name', required=True)

    class Meta:
        model = Guest
        # Use 'first_name' and 'last_name' here to match the frontend's input structure
        fields = ['first_name', 'last_name', 'email', 'phone', 'vat', 'adult']
        extra_kwargs = {
            'email': {'validators': []} # Temporarily disable unique validation at serializer level if causing issues during get_or_create logic,
                                        # but keep it on the model for database integrity.
                                        # Only do this if you understand the implications and have robust model-level unique handling.
        }


class ReservationSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new Reservation instance.
    Handles the creation/linking of main_guest and other_guests.
    """
    # These fields are for the main guest details from the frontend
    guest_first_name = serializers.CharField(write_only=True, required=True)
    guest_last_name = serializers.CharField(write_only=True, required=True)
    guest_email = serializers.EmailField(write_only=True, required=False, allow_blank=True)
    guest_phone = serializers.CharField(write_only=True, required=False, allow_blank=True)
    guest_vat = serializers.CharField(write_only=True, required=False, allow_blank=True)
    guest_adult = serializers.BooleanField(write_only=True, required=True)

    # This handles the list of additional guests
    # Make required=False because 'additional_guests' might be empty, as shown in your JSON
    guests_details = GuestSerializer(many=True, write_only=True, required=False)

    daily_rate = serializers.DecimalField(max_digits=8, decimal_places=2, required=False)

    class Meta:
        model = Reservation
        fields = [
            'check_in_date',
            'check_out_date',
            'special_requests',
            'daily_rate',
            # Include these "extra" fields that map to main guest details
            'guest_first_name',
            'guest_last_name',
            'guest_email',
            'guest_phone',
            'guest_vat',
            'guest_adult',
            # Include this for the list of additional guests
            'guests_details',
        ]
        # Ensure main_guest is treated as read-only for input purposes,
        # as we are setting it manually in the .create() method.
        # It will be included in the output when serialization happens.
        read_only_fields = [
            'status',
            'reservation_date',
            'last_updated',
            'total_guests',
            'total_price',
            'payment_status',
            'payment_transaction_id',
            'deposit_amount',
            'is_email_verified',
            'main_guest',   # Critical: Keep this here. It means 'main_guest' won't be expected in input.
            'other_guests', # Critical: Keep this here. Same reason as main_guest.
        ]


    def validate(self, data):
        """
        Custom validation for the entire reservation data.
        """
        check_in_date = data.get('check_in_date')
        check_out_date = data.get('check_out_date')

        # Combine main guest details and additional guests for consolidated adult count
        all_guests_for_validation = []

        # Add main guest details if present
        if data.get('guest_email'): # Check if main guest email is provided
            all_guests_for_validation.append({
                'adult': data.get('guest_adult', True), # Default to True for main guest
                'email': data['guest_email'] # Only need email for uniqueness check if required
            })

        # Add details of additional guests
        for guest_detail in data.get('guests_details', []):
            all_guests_for_validation.append({
                'adult': guest_detail.get('adult', True),
                'email': guest_detail.get('email')
            })

        if not all_guests_for_validation:
            raise serializers.ValidationError(
                {"guests": _("At least one guest (main guest) is required for the reservation.")}
            )

        # Ensure at least one adult among all guests
        num_adults_calculated = sum(1 for g in all_guests_for_validation if g.get('adult'))
        if num_adults_calculated < 1:
            raise serializers.ValidationError(
                {"num_adults": _("The reservation must include at least one adult.")}
            )

        # Date validations
        if check_in_date and check_out_date:
            if check_out_date <= check_in_date:
                raise serializers.ValidationError(
                    {"check_out_date": _("Check-out date must be after check-in date.")}
                )
            # if check_in_date < timezone.localdate():
            #     raise serializers.ValidationError(
            #         {"check_in_date": _("Check-in date cannot be in the past.")}
            #     )

        return data


    def create(self, validated_data):
        print("\n\n\n validated_data at start of create:", validated_data)

        # 1. Pop all guest-related data that won't be directly on Reservation model
        main_guest_data = {
            'name': validated_data.pop('guest_first_name'),
            'last_name': validated_data.pop('guest_last_name'),
            'email': validated_data.pop('guest_email'),
            'phone': validated_data.pop('guest_phone', ''),
            'vat': validated_data.pop('guest_vat', ''),
            'adult': validated_data.pop('guest_adult', True),
        }
        additional_guests_data = validated_data.pop('guests_details', []) # Pop with default empty list

        # 2. Handle Main Guest (get or create)
        try:
            main_guest, created = Guest.objects.get_or_create(
                email=main_guest_data['email'],
                defaults=main_guest_data
            )
            if not created: # If guest already exists, update their details
                for attr, value in main_guest_data.items():
                    setattr(main_guest, attr, value)
                main_guest.full_clean() # Run model's clean method
                main_guest.save()
        except Exception as e:
            raise serializers.ValidationError(f"Error processing main guest: {e}")

        # Initialize counts
        num_adults_total = 0
        num_children_total = 0

        if main_guest.adult:
            num_adults_total += 1
        else:
            num_children_total += 1

        # 3. Handle Other Guests (get or create)
        other_guests_objects = []
        for guest_data in additional_guests_data:
            # Map 'first_name' to 'name' for the Guest model
            guest_model_data = {
                'name': guest_data.get('name'),
                'last_name': guest_data.get('last_name'),
                'email': guest_data.get('email', ''),
                'phone': guest_data.get('phone', ''),
                'vat': guest_data.get('vat', ''),
                'adult': guest_data.get('adult', True),
            }
            try:
                guest, created = Guest.objects.get_or_create(
                    email=guest_model_data['email'],
                    defaults=guest_model_data
                )
                if not created: # If guest already exists, update details
                    for attr, value in guest_model_data.items():
                        setattr(guest, attr, value)
                    guest.full_clean()
                    guest.save()
            except Exception as e:
                raise serializers.ValidationError(f"Error processing additional guest '{guest_model_data.get('email', 'N/A')}': {e}")

            other_guests_objects.append(guest)

            if guest.adult:
                num_adults_total += 1
            else:
                num_children_total += 1

        # 4. Create the Reservation instance
        # 'validated_data' now only contains fields directly belonging to Reservation model
        reservation = Reservation.objects.create(
            main_guest=main_guest,
            num_adults=num_adults_total,
            num_children=num_children_total,
            total_guests=num_adults_total + num_children_total,
            daily_rate=1,
            total_price=1.,
            **validated_data
        )

        # 5. Set ManyToMany relationship for other guests
        if other_guests_objects:
            reservation.other_guests.set(other_guests_objects)

        # 6. Calculate total_price
        if reservation.check_in_date and reservation.check_out_date and reservation.daily_rate:
            num_nights = (reservation.check_out_date - reservation.check_in_date).days
            if num_nights > 0:
                reservation.total_price = reservation.daily_rate * num_nights
            else:
                reservation.total_price = 0
        else:
            reservation.total_price = 0

        # Save again to persist calculated fields like total_price, total_guests
        reservation.full_clean() # Run model's clean method (which also updates total_guests)
        reservation.save()

        print("\n\n\n Reservation object successfully created:", reservation)

        


        
        name = main_guest_data['name']
        mail = main_guest_data['email']
        message = "ddd"
        subject = f"Casa do Santo/Formulario Contacto"
        mail_body = f"""
            El/la señor/a {name} ha hecho una reserva: \n
            {message}\n
            Por favor respondedle lo antes posible al correo {mail}
        """
        recipient_list = ["casadosantocoira@gmail.com"]

        try:
            send_mail(
                subject,
                mail_body,
                "casadosantocoira@gmail.com",  # From email (configured in settings)
                recipient_list,  # To email(s)
                fail_silently=False,  # Raise errors if sending fails
                # Optional: To make 'Reply-To' work correctly in email clients
                # headers={'Reply-To': from_email}
            )
        except Exception as e:
            print("error:", e)
            return JsonResponse({"message": str(e)})




        return reservation