from rest_framework import serializers
from .models import Reservation, Guest # Make sure to import Guest as well
from django.utils import timezone # For validation


# --- 1. Define a Guest Serializer for Nested Display ---
# This serializer will be used to display details of the main_guest and other_guests.
class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['id', 'name', 'last_name', 'email', 'phone', 'vat']
        read_only_fields = ['id'] # IDs are usually read-only for nested objects


# --- 2. Update the Reservation Serializer ---
class ReservationSerializer(serializers.ModelSerializer):
    # --- Read Operations (for GET requests) ---
    # Display the full Guest object for main_guest
    main_guest = GuestSerializer(read_only=True)
    # Display a list of full Guest objects for other_guests
    other_guests = GuestSerializer(many=True, read_only=True)

    # --- Write Operations (for POST, PUT, PATCH requests) ---
    # Accept the ID of the main guest for creating/updating a reservation.
    # 'source' maps this field to the actual 'main_guest' ForeignKey on the model.
    # 'write_only=True' ensures this field is only for input, not output.
    main_guest_id = serializers.PrimaryKeyRelatedField(
        queryset=Guest.objects.all(), # Required: Django needs to know which Guests are valid
        source='main_guest',
        write_only=True,
        required=True, # Assuming main_guest is mandatory for a reservation
        allow_null=False # If main_guest can be blank/null, set to True
    )

    # Accept a list of IDs for other guests (ManyToMany).
    # 'many=True' is crucial for ManyToMany relationships.
    other_guest_ids = serializers.PrimaryKeyRelatedField(
        queryset=Guest.objects.all(), # Required: Django needs to know which Guests are valid
        source='other_guests',
        many=True,
        write_only=True,
        required=False, # other_guests is blank=True on the model
    )

    class Meta:
        model = Reservation
        # Fields for both input and output (common fields)
        fields = [
            'check_in_date', 'check_out_date', 'num_adults', 'num_children',
            'special_requests',
            # Fields for relationship output (read-only)
            'main_guest',
            'other_guests',
            # Fields for relationship input (write-only)
            'main_guest_id',
            'other_guest_ids',
            # Read-only fields (calculated or backend-managed)
            'total_guests', 'daily_rate', 'total_price', 'payment_status',
            'status', 'reservation_date', 'last_updated',
            'payment_transaction_id', 'deposit_amount', 'is_email_verified'
        ]
        # All fields listed in 'read_only_fields' here must also be in 'fields' above.
        # It's usually better to list all fields and then use `read_only=True` for specific serializer fields.
        # Or, as done above, list output fields directly as read_only in the serializer definition,
        # and list other read-only fields here.
        read_only_fields = [
            'total_guests', 'daily_rate', 'total_price', 'payment_status',
            'status', 'reservation_date', 'last_updated',
            'payment_transaction_id', 'deposit_amount', 'is_email_verified'
        ]


    def validate(self, data):
        # Validation for check-out date vs check-in date
        if data['check_out_date'] <= data['check_in_date']:
            raise serializers.ValidationError(
                {"check_out_date": _("Check-out date must be after check-in date.")}
            )

        # Validation for check-in date not in the past
        # Use timezone.localdate() for current date comparison
        if data['check_in_date'] < timezone.localdate():
            raise serializers.ValidationError(
                {"check_in_date": _("Check-in date cannot be in the past.")}
            )

        # Ensure minimum 1 adult
        if data['num_adults'] < 1:
            raise serializers.ValidationError(
                {"num_adults": _("There must be at least one adult in the reservation.")}
            )

        # Assuming main_guest_id is passed, you can validate the existence of the guest if needed
        # Although PrimaryKeyRelatedField already handles basic existence,
        # you might add custom logic here if specific guest properties are required.

        # You might also want to add availability check here.
        # This typically requires the instance (for updates) or just the dates (for creation)
        # and database queries to other reservations.
        # Example (simplified):
        # if not self.instance: # Only for new reservations
        #     # You'd need a more robust availability check method, perhaps on the model manager
        #     # For example: Reservation.objects.check_availability(data['check_in_date'], data['check_out_date'])
        #     if not Reservation().is_house_available(data['check_in_date'], data['check_out_date']):
        #         raise serializers.ValidationError({"dates": _("House is not available for these dates.")})
        # else: # For existing reservations, check availability excluding self
        #     if not self.instance.is_house_available(data['check_in_date'], data['check_out_date']):
        #         raise serializers.ValidationError({"dates": _("House is not available for these dates.")})


        return data

    def create(self, validated_data):
        # DRF's ModelSerializer typically handles PrimaryKeyRelatedField (with source)
        # correctly for create and update operations.
        # The main_guest and other_guests relationships will be set automatically
        # based on the main_guest_id and other_guest_ids fields.

        # daily_rate, total_price, total_guests, payment_status, status
        # will be set by the model's clean() and save() methods.

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # DRF's ModelSerializer also handles updates for PrimaryKeyRelatedField with source.
        # For ManyToMany fields (like other_guests), .set() is often used internally.
        # If you had complex logic for updating related ManyToMany fields,
        # you might need to extract 'other_guests' from validated_data, call super().update(),
        # and then manually update 'instance.other_guests.set(other_guests_list)'.
        # However, with 'source', DRF often handles this automatically.

        return super().update(instance, validated_data)