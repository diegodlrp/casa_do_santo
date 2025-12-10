from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import datetime
import uuid


# Create your models here.
class Guest(models.Model):
    """
    Model to store individual guest's contact and personal information.
    """

    DOCUMENT_TYPES = [
        ("NIF", "NIF"),
        ("DNI", "DNI"),
        ("NIE", "NIE"),
        ("PASSPORT", "Passport"),
        ("DRIVING_LICENSE", "Driving License"),
    ]

    SEX_TYPES = [
        ("male", "Hombre"),
        ("female", "Mujer"),
    ]

    name = models.CharField(max_length=100, verbose_name=_("Nombre"))
    last_name = models.CharField(
        max_length=100, null=True, blank=True, verbose_name=_("Primer apellido")
    )
    last_name2 = models.CharField(
        max_length=100,
        verbose_name=_("Segundo apellido"),
        null=True,
        blank=True,
    )
    email = models.EmailField(
        verbose_name=_("Email"),
        null=True,
        blank=True,
    )  # Make email unique for better lookup
    phone = models.CharField(
        max_length=20, null=True, blank=True, verbose_name=_("Teléfono")
    )
    mobile = models.CharField(
        max_length=20, null=True, blank=True, verbose_name=_("Móbil")
    )
    vat = models.CharField(max_length=20,  null=True, blank=True, verbose_name=_("Nº de documento"))

    # Changed verbose_name for clarity
    document_type = models.CharField(
        max_length=100,
        choices=DOCUMENT_TYPES,
        default="NIF",
        verbose_name=_("Tipo de Documento"),
    )
    nacionality = models.CharField(
        max_length=100,
        verbose_name=_("Nacionalidad"),
        null=True,
        blank=True,
    )
    address = models.CharField(
        max_length=100,
        verbose_name=_("Dirección"),
        null=True,
        blank=True,
    )
    address_state = models.CharField(
        max_length=100,
        verbose_name=_("Provincia/Estado"),
        null=True,
        blank=True,
    )
    country = models.CharField(
        max_length=100,
        verbose_name=_("Pais"),
        null=True,
        blank=True,
    )
    adult = models.BooleanField(
        verbose_name=_("Adulto"),
        null=True,
        blank=True,
    )

    sex = models.CharField(
        max_length=100,
        choices=SEX_TYPES,
        verbose_name=_("Sexo"),
        null=True,
        blank=True,
    )

    birth_date = models.DateField(
        verbose_name=_("Fecha nacimiento"),
        null=True,
        blank=True,
    )

    documment_support = models.CharField(
        max_length=100,
        verbose_name=_("Soporte del documento"),
        null=True,
        blank=True,
    )
    zip = models.CharField(
        max_length=100,
        verbose_name=_("Código postal"),
        null=True,
        blank=True,
    )
        # verbose_name=_("Parentesco"),ue512021
# 
    relationship = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Huesped")
        verbose_name_plural = _("Huespedes")
        # Add a unique_together constraint if a guest can be uniquely identified by name + last_name + email
        # unique_together = ('name', 'last_name', 'email')
        ordering = ["name", "vat"]

    def __str__(self):
        return f"{self.name} {self.last_name} ({self.email})"


class Reservation(models.Model):
    """
    Handles booking/reservation for the entire house
    """

    STATUS_CHOICES = (
        ("pending", _("Pendiente")),
        ("confirmed", _("Confirmado")),
        ("checked_in", _("Check In")),
        ("checked_out", _("Check Out")),
        ("cancelled", _("Cancelado")),
        ("no_show", _("No Show")),
    )

    # --- PRIMARY GUEST REFERENCE ---
    # The main guest making the reservation is now linked via ForeignKey.
    # This replaces guest_first_name, guest_last_name, guest_email, guest_phone.
    main_guest = models.ForeignKey(
        Guest,
        on_delete=models.CASCADE,
        related_name="main_reservations",  # Renamed related_name for clarity
        verbose_name=_("Huesped principal"),
    )

    # --- OTHER GUESTS REFERENCE ---
    # Multiple other guests can be associated with this reservation.
    other_guests = models.ManyToManyField(
        Guest,
        blank=True,
        related_name="other_reservations",  # Renamed for clarity
        verbose_name=_("Otros Huespedes"),
    )

    # Information about the primary guest making the reservation
    # >>> THESE FIELDS ARE NOW REMOVED/OBSOLETE <<<
    # guest_first_name = models.CharField(max_length=100, verbose_name=_("Guest First Name"))
    # guest_last_name = models.CharField(max_length=100, verbose_name=_("Guest Last Name"))
    # guest_email = models.EmailField(verbose_name=_("Guest Email"))
    # guest_phone = models.CharField(max_length=20, blank=True, verbose_name=_("Guest Phone"))

    # Reservation period
    check_in_date = models.DateField(verbose_name=_("Fecha Check-in"))
    check_out_date = models.DateField(verbose_name=_("Fecha Check-out"))

    # Guest count for the whole house
    num_adults = models.PositiveIntegerField(
        blank=True, default=1, verbose_name=_("Numero de Adultos")
    )
    num_children = models.PositiveIntegerField(
        blank=True, default=0, verbose_name=_("Numero de Niños")
    )
    total_guests = models.PositiveIntegerField(
        blank=True, null=True, verbose_name=_("Nº Total (Calculado)")
    )  # Stored for convenience

    # Pricing and payment details
    daily_rate = models.DecimalField(
        max_digits=8,
        blank=True,
        null=True,
        decimal_places=2,
        verbose_name=_("Daily Rate at Booking"),
    )
    total_price = models.DecimalField(
        max_digits=10,
        blank=True,
        null=True,
        decimal_places=2,
        verbose_name=_("Total Price"),
    )
    payment_status = models.CharField(
        max_length=20,
        choices=(
            ("pending", _("Pendiente")),
            ("paid", _("Pagado")),
            ("refunded", _("Devuelto")),
            ("failed", _("Fallo")),
        ),
        default="pending",
        verbose_name=_("Estado del pago"),
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
        verbose_name=_("Deposito"),
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
        verbose_name=_("Estado"),
    )
    reservation_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Fecha Reserva")
    )
    last_updated = models.DateTimeField(
        auto_now=True, verbose_name=_("Última actualización")
    )

    class Meta:
        verbose_name = _("Reserva")
        verbose_name_plural = _("Reservas")
        ordering = ["check_in_date", "check_out_date"]

    def __str__(self):
        # Now uses the main_guest's name
        if self.main_guest:
            return f"Reservation for {self.main_guest.name} {self.main_guest.last_name} from {self.check_in_date} to {self.check_out_date}"
        return f"Reservation (ID: {self.pk}) from {self.check_in_date} to {self.check_out_date}"

    # def clean(self):
    #     """
    #     Custom validation for the Reservation model.
    #     """
    #     # Ensure check-out date is after check-in date
    #     if self.check_in_date and self.check_out_date:
    #         if self.check_out_date <= self.check_in_date:
    #             raise ValidationError(_("Check-out date must be after check-in date."))

    #     # Corrected: Use 'total_guests' (plural) matching your model field name
    #     self.total_guests = self.num_adults + self.num_children

    #     # Ensure minimum 1 adult
    #     if self.num_adults < 1:
    #         raise ValidationError(
    #             _("There must be at least one adult in the reservation.")
    #         )

    #     # Prevent booking in the past
    #     if self.check_in_date and self.check_in_date < datetime.date.today():
    #         raise ValidationError(_("Check-in date cannot be in the past."))

    #     # Calculate total price (can be done here or in save/signal)
    #     # Ensure num_nights is calculated first if dates are set
    #     if (
    #         self.daily_rate and self.check_in_date and self.check_out_date
    #     ):  # Ensure dates are present for num_nights
    #         self.total_price = self.daily_rate * 3
    #     else:
    #         self.total_price = 0  # Default if dates/rate not set yet


class ReservationEditToken(models.Model):
    token = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    used = models.BooleanField(default=False)

    def __str__(self):
        return f"Token for {self.reservation}"


class DailyPrice(models.Model):
    date = models.DateField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1)

    def __str__(self):
        return f"{self.date}: {self.price}"


class Discount(models.Model):
    days_number = models.PositiveIntegerField()
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    percentage = models.BooleanField(default=True)

class DateRangeMinDays(models.Model):
    """
    Represents a discount that applies to a specific date range,
    with a minimum number of days required.
    """
    start_date = models.DateField(verbose_name=_("Start Date"))
    end_date = models.DateField(verbose_name=_("End Date"))
    min_days = models.PositiveIntegerField(
        verbose_name=_("Minimum Days"),
        
    )