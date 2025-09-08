from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import datetime

# Create your models here.


class Guest(models.Model):
    """
    Model to store individual guest's contact and personal information.
    """

    DOCUMENT_TYPES = [
        ('NIF', 'NIF'),
        ('DNI', 'DNI'),
        ('NIE', 'NIE'),
        ('PASSPORT', 'Passport'),
        ('DRIVING_LICENSE', 'Driving License'),
    ]

    name = models.CharField(max_length=100, verbose_name=_("Guest First Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Guest Last Name"))
    last_name2 = models.CharField(max_length=100, verbose_name=_("Guest Last Name"), default="")
    email = models.EmailField(
        verbose_name=_("Guest Email"), blank=True
    )  # Make email unique for better lookup
    phone = models.CharField(max_length=20, blank=True, verbose_name=_("Guest Phone"))
    mobile = models.CharField(max_length=20, blank=True, verbose_name=_("Guest Phone"))
    vat = models.CharField(
        max_length=20, blank=True, verbose_name=_("Guest VAT/Tax ID")
    )  # Changed verbose_name for clarity
    document_type = models.CharField(
        max_length=100,
        choices=DOCUMENT_TYPES,
        default='NIF',
        verbose_name=_("Document Type")
    )
    nacionality = models.CharField(max_length=100, verbose_name=_("Nacionality"), default="")
    address = models.CharField(max_length=100, verbose_name=_("Guest Address"), default="")
    address_state = models.CharField(max_length=100, verbose_name=_("Guest State"), default="")
    country = models.CharField(max_length=100, verbose_name=_("Guest Country"), default="")
    adult = models.BooleanField(verbose_name=_("Guest adult"))

    class Meta:
        verbose_name = _("Guest")
        verbose_name_plural = _("Guests")
        # Add a unique_together constraint if a guest can be uniquely identified by name + last_name + email
        # unique_together = ('name', 'last_name', 'email')
        ordering = ["last_name", "name"]

    def __str__(self):
        return f"{self.name} {self.last_name} ({self.email})"


class Reservation(models.Model):
    """
    Handles booking/reservation for the entire house
    """

    STATUS_CHOICES = (
        ("pending", _("Pending")),
        ("confirmed", _("Confirmed")),
        ("checked_in", _("Checked In")),
        ("checked_out", _("Checked Out")),
        ("cancelled", _("Cancelled")),
        ("no_show", _("No Show")),
    )

    # --- PRIMARY GUEST REFERENCE ---
    # The main guest making the reservation is now linked via ForeignKey.
    # This replaces guest_first_name, guest_last_name, guest_email, guest_phone.
    main_guest = models.ForeignKey(
        Guest,
        on_delete=models.SET_NULL,  # If the Guest record is deleted, set this field to NULL
        null=True,  # Allow a reservation to exist without a main_guest (e.g., if deleted)
        blank=True,  # Allow the field to be optional in forms/admin
        related_name="main_reservations",  # Renamed related_name for clarity
        verbose_name=_("Main Guest"),
    )

    # --- OTHER GUESTS REFERENCE ---
    # Multiple other guests can be associated with this reservation.
    other_guests = models.ManyToManyField(
        Guest,
        blank=True,
        related_name="other_reservations",  # Renamed for clarity
        verbose_name=_("Other Guests"),
    )

    # Information about the primary guest making the reservation
    # >>> THESE FIELDS ARE NOW REMOVED/OBSOLETE <<<
    # guest_first_name = models.CharField(max_length=100, verbose_name=_("Guest First Name"))
    # guest_last_name = models.CharField(max_length=100, verbose_name=_("Guest Last Name"))
    # guest_email = models.EmailField(verbose_name=_("Guest Email"))
    # guest_phone = models.CharField(max_length=20, blank=True, verbose_name=_("Guest Phone"))

    # Reservation period
    check_in_date = models.DateField(verbose_name=_("Check-in Date"))
    check_out_date = models.DateField(verbose_name=_("Check-out Date"))

    # Guest count for the whole house
    num_adults = models.PositiveIntegerField(
        default=1, verbose_name=_("Number of Adults")
    )
    num_children = models.PositiveIntegerField(
        default=0, verbose_name=_("Number of Children")
    )
    total_guests = models.PositiveIntegerField(
        verbose_name=_("Total Guests (Calculated)")
    )  # Stored for convenience

    # Pricing and payment details
    daily_rate = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name=_("Daily Rate at Booking")
    )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Total Price")
    )
    payment_status = models.CharField(
        max_length=20,
        choices=(
            ("pending", _("Pending")),
            ("paid", _("Paid")),
            ("refunded", _("Refunded")),
            ("failed", _("Failed")),
        ),
        default="pending",
        verbose_name=_("Payment Status"),
    )
    payment_transaction_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        verbose_name=_("Payment Transaction ID"),
    )
    deposit_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Deposit Amount"),
    )
    is_email_verified = models.BooleanField(
        default=False, verbose_name=_("Email Verified")
    )

    # Special requests or notes
    special_requests = models.TextField(blank=True, verbose_name=_("Special Requests"))

    # Status and timestamps
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name=_("Status"),
    )
    reservation_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Reservation Date")
    )
    last_updated = models.DateTimeField(auto_now=True, verbose_name=_("Last Updated"))

    class Meta:
        verbose_name = _("House Reservation")
        verbose_name_plural = _("House Reservations")
        ordering = ["check_in_date", "check_out_date"]

    def __str__(self):
        # Now uses the main_guest's name
        if self.main_guest:
            return f"Reservation for {self.main_guest.name} {self.main_guest.last_name} from {self.check_in_date} to {self.check_out_date}"
        return f"Reservation (ID: {self.pk}) from {self.check_in_date} to {self.check_out_date}"

    def clean(self):
        """
        Custom validation for the Reservation model.
        """
        # Ensure check-out date is after check-in date
        if self.check_in_date and self.check_out_date:
            if self.check_out_date <= self.check_in_date:
                raise ValidationError(_("Check-out date must be after check-in date."))

        # Corrected: Use 'total_guests' (plural) matching your model field name
        self.total_guests = self.num_adults + self.num_children

        # Ensure minimum 1 adult
        if self.num_adults < 1:
            raise ValidationError(
                _("There must be at least one adult in the reservation.")
            )

        # Prevent booking in the past
        if self.check_in_date and self.check_in_date < datetime.date.today():
            raise ValidationError(_("Check-in date cannot be in the past."))

        # Calculate total price (can be done here or in save/signal)
        # Ensure num_nights is calculated first if dates are set
        if (
            self.daily_rate and self.check_in_date and self.check_out_date
        ):  # Ensure dates are present for num_nights
            self.total_price = self.daily_rate * 3
        else:
            self.total_price = 0  # Default if dates/rate not set yet

class DailyPrice(models.Model):
    date = models.DateField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    
    def __str__(self):
        return f"{self.date}: {self.price}"

class Discount(models.Model):
    days_number = models.PositiveIntegerField()
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    percentage = models.BooleanField(default=True)
