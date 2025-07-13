from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import datetime

# Create your models here.
class Reservation(models.Model):
    """
    Handles booking/reservation for the entire house
    """

    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('confirmed',  _('Confirmed')),
        ('checked_in', _('Checked In')),
        ('checked_out', _('Checked Out')),
        ('cancelled', _('Cancelled')),
        ('no_show', _('No Show'))
    )

    # Information about the primary guest making the reservation
    guest_first_name = models.CharField(max_length=100, verbose_name=_("Guest First Name"))
    guest_last_name = models.CharField(max_length=100, verbose_name=_("Guest Last Name"))
    guest_email = models.EmailField(verbose_name=_("Guest Email"))
    guest_phone = models.CharField(max_length=20, blank=True, verbose_name=_("Guest Phone"))

    # Reservation period
    check_in_date = models.DateField(verbose_name=_("Check-in Date"))
    check_out_date = models.DateField(verbose_name=_("Check-out Date"))

    # Guest count for the whole house
    num_adults = models.PositiveIntegerField(default=1, verbose_name=_("Number of Adults"))
    num_children = models.PositiveIntegerField(default=0, verbose_name=_("Number of Children"))
    total_guests = models.PositiveIntegerField(verbose_name=_("Total Guests (Calculated)")) # Stored for convenience

    # Pricing and payment details
    daily_rate = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_("Daily Rate at Booking")
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Total Price")
    )
    payment_status = models.CharField(
        max_length=20,
        choices=(
            ('pending', _('Pending')),
            ('paid', _('Paid')),
            ('refunded', _('Refunded')),
            ('failed', _('Failed')),
        ),
        default='pending',
        verbose_name=_("Payment Status")
    )
    payment_transaction_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        verbose_name=_("Payment Transaction ID")
    )
    deposit_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Deposit Amount")
    )
    is_email_verified = models.BooleanField(default=False, verbose_name=_("Email Verified"))


    # Special requests or notes
    special_requests = models.TextField(blank=True, verbose_name=_("Special Requests"))

    # Status and timestamps
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_("Status")
    )
    reservation_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Reservation Date"))
    last_updated = models.DateTimeField(auto_now=True, verbose_name=_("Last Updated"))

    class Meta:
        verbose_name = _("House Reservation")
        verbose_name_plural = _("House Reservations")
        ordering = ['check_in_date', 'check_out_date']

    def __str__(self):
        return f"Reservation for {self.guest_first_name} {self.guest_last_name} from {self.check_in_date} to {self.check_out_date}"

    def clean(self):
        """
        Custom validation for the Reservation model.
        """
        # Ensure check-out date is after check-in date
        if self.check_in_date and self.check_out_date:
            if self.check_out_date <= self.check_in_date:
                raise ValidationError(
                    _("Check-out date must be after check-in date.")
                )

        # Ensure minimum 1 adult
        if self.num_adults < 1:
            raise ValidationError(
                _("There must be at least one adult in the reservation.")
            )

        # Prevent booking in the past
        if self.check_in_date and self.check_in_date < datetime.date.today():
            raise ValidationError(
                _("Check-in date cannot be in the past.")
            )

        # Calculate total guests
        self.total_guests = self.num_adults + self.num_children

        # Calculate total price (can be done here or in save/signal)
        if self.daily_rate and self.num_nights > 0:
            self.total_price = self.daily_rate * self.num_nights
        else:
            self.total_price = 0 # Default if dates/rate not set yet


    def save(self, *args, **kwargs):
        """
        Override save to run full validation and calculate derived fields.
        """
        self.full_clean() # Calls clean() and validates all fields
        super().save(*args, **kwargs)

    @property
    def num_nights(self):
        """Calculates the number of nights for the reservation."""
        if self.check_in_date and self.check_out_date:
            return (self.check_out_date - self.check_in_date).days
        return 0

    # You might add a method here to check for overlaps
    def is_house_available(self, check_in, check_out):
        """
        Checks if the house is available for the given dates.
        This is a crucial logic that would be handled in views/serializers,
        but a method here can help for initial checks.
        """
        # Exclude current reservation if updating
        conflicting_reservations = Reservation.objects.filter(
            check_in_date__lt=check_out, # Check-in before desired check-out
            check_out_date__gt=check_in,  # Check-out after desired check-in
        ).exclude(pk=self.pk if self.pk else None) # Exclude self if updating

        return not conflicting_reservations.exists()