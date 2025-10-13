# reservations_app/serializers.py

# --- 1. Python Standard Library Imports ---
import json
from io import BytesIO # UNUSUAL for serializers, typically used in views/utility functions

# --- 2. Third-Party Imports ---
from rest_framework import serializers

# UNUSUAL for serializers, these are for PDF generation, which belongs in a utility or view file
from reportlab.pdfgen import canvas 

# --- 3. Django Core/Contributed Imports ---
from django.core.mail import send_mail            # UNUSUAL for serializers, usually handled in tasks or service/utility layer
from django.db import transaction                  # GOOD: Needed for atomic operations in create/update logic
from django.http import FileResponse, JsonResponse # UNUSUAL: These are for views, not serializers
from django.shortcuts import render                # UNUSUAL: For rendering templates in views
from django.utils.translation import gettext_lazy as _ # GOOD: For translatable field labels/messages

# UNUSUAL: These are view decorators, which belong in views.py
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST 

# --- 4. Local App Imports ---
from .models import Guest, Reservation, Discount, ReservationEditToken # GOOD: Necessary for defining the serializer fields


class GuestSerializer(serializers.ModelSerializer):
    """
    Serializer for the Guest model, used for nested operations within Reservation.
    """

    # Your Guest model has 'name' and 'last_name'. Your frontend sends 'first_name' and 'last_name'.
    # This maps 'first_name' from the incoming JSON to the 'name' field of the Guest model.
    # name = serializers.CharField(source="name", required=True)

    class Meta:
        model = Guest
        # Use 'first_name' and 'last_name' here to match the frontend's input structure
        fields = ["name", "vat", "document_type", "email"]
        extra_kwargs = {
            "email": {
                "validators": []
            }  # Temporarily disable unique validation at serializer level if causing issues during get_or_create logic,
            # but keep it on the model for database integrity.
            # Only do this if you understand the implications and have robust model-level unique handling.
        }


class ReservationSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new Reservation instance.
    Handles the creation/linking of main_guest and other_guests.
    """

    class Meta:
        model = Reservation
        fields = [
            "check_in_date",
            "check_out_date",
            "special_requests",
            "main_guest",
            "total_guests",
            "num_children",
            "num_adults",
        ]


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = "__all__"
