# reservations_app/serializers.py
from rest_framework import serializers
from .models import Guest, Reservation, Discount
from django.utils.translation import gettext_lazy as _
from django.db import transaction  # Needed for atomic operations in create
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
    # name = serializers.CharField(source="name", required=True)

    class Meta:
        model = Guest
        # Use 'first_name' and 'last_name' here to match the frontend's input structure
        fields = ["name", "vat", "document_type"]
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
