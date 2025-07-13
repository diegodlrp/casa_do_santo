from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Reservation 

# Register your models here.
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'guest_first_name', 'guest_last_name', 'check_in_date',
        'check_out_date', 'status', 'total_guests', 'daily_rate', 'total_price',
        'payment_status', 'is_email_verified'
    )
    list_filter = ('status', 'check_in_date', 'check_out_date', 'payment_status')
    search_fields = ('guest_first_name', 'guest_last_name', 'guest_email', 'guest_phone', 'payment_transaction_id')
    readonly_fields = ('reservation_date', 'last_updated', 'total_guests', 'total_price') # Total price is calculated

    # If you want to allow manual daily_rate adjustment in admin, keep it writable.
    # Otherwise, you might set it as readonly_fields and manage its default value elsewhere.
    fieldsets = (
        (_('Guest Details'), {
            'fields': ('guest_first_name', 'guest_last_name', 'guest_email', 'guest_phone', 'is_email_verified')
        }),
        (_('Reservation Details'), {
            'fields': ('check_in_date', 'check_out_date', 'num_adults', 'num_children', 'special_requests')
        }),
        (_('Pricing & Payment'), {
            'fields': ('daily_rate', 'total_price', 'payment_status', 'deposit_amount', 'payment_transaction_id')
        }),
        (_('Status & Timestamps'), {
            'fields': ('status', 'reservation_date', 'last_updated', 'total_guests')
        }),
    )

    def save_model(self, request, obj, form, change):
        # Ensure total_price is calculated before saving in the admin
        obj.total_price = 12#obj.calculate_total_price() # Or rely on obj.full_clean()
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Ensure calculated fields are not editable in admin, but displayed
        if obj: # For existing objects, make total_price read-only
             form.base_fields['total_price'].disabled = True
        return form