from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Reservation, Guest # Ensure Guest is imported

# Register your models here.
@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'email', 'phone', 'vat')
    search_fields = ('name', 'last_name', 'email', 'phone', 'vat')
    list_filter = ('name', 'last_name') # Basic filters
    ordering = ('last_name', 'name') # Consistent with model Meta


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'main_guest', # Displays the __str__ of the Guest object
        'check_in_date',
        'check_out_date',
        'status',
        'total_guests',
        'daily_rate',
        'total_price',
        'payment_status',
        'is_email_verified',
        'get_other_guests_count' # Custom method for list_display
    )
    list_filter = ('status', 'check_in_date', 'check_out_date', 'payment_status')

    # IMPORTANT: For ForeignKey and ManyToMany fields in search_fields,
    # you need to use the double underscore (__) to traverse relationships.
    search_fields = (
        'main_guest__name',         # Search by main guest's first name
        'main_guest__last_name',    # Search by main guest's last name
        'main_guest__email',        # Search by main guest's email
        'payment_transaction_id',   # Your existing field
        'special_requests',         # Often useful to search here too
    )

    # Fields that should not be editable in the admin form
    readonly_fields = (
        'reservation_date',
        'last_updated',
        'total_guests', # Calculated in model's clean/save
        'total_price'   # Calculated in model's clean/save
    )

    # `filter_horizontal` is great for ManyToMany fields for better UX
    filter_horizontal = ('other_guests',) # Use the correct plural name

    fieldsets = (
        (_('Guest Details'), {
            'fields': ('main_guest', 'other_guests') # Use the correct plural name
        }),
        (_('Reservation Details'), {
            'fields': ('check_in_date', 'check_out_date', 'num_adults', 'num_children', 'special_requests')
        }),
        (_('Pricing & Payment'), {
            'fields': ('daily_rate', 'payment_status', 'deposit_amount', 'payment_transaction_id')
            # total_price is now in readonly_fields, so remove it from here
        }),
        (_('Status & Timestamps'), {
            'fields': ('status', 'reservation_date', 'last_updated', 'total_guests', 'total_price')
            # total_guests and total_price are in readonly_fields, but still need to be listed here
            # if you want them to appear in this fieldset.
        }),
    )

    # --- Custom Methods for Admin List Display ---
    def get_other_guests_count(self, obj):
        return obj.num_adults + obj.num_children
        
    get_other_guests_count.short_description = _("Other Guests Count")
    get_other_guests_count.admin_order_field = 'other_guests__count' # Allows sorting by count (requires Django 2.0+)

    # --- Overriding save_model ---
    # You generally don't need to override save_model for calculations
    # if your model's clean() and save() methods already handle them.
    # obj.full_clean() is called within obj.save() by default, which
    # runs your clean() method where total_price and total_guests are calculated.
    # So, simply calling super().save_model() is usually sufficient.
    def save_model(self, request, obj, form, change):
        # The obj.full_clean() in your model's save() method will calculate
        # total_price and total_guests before saving.
        super().save_model(request, obj, form, change)

    # --- Overriding get_form ---
    # This override is now redundant for 'total_price' because it's in `readonly_fields`.
    # `readonly_fields` is the standard and simpler way to make fields read-only in the admin.
    # If you had other, more complex form manipulations, you'd keep this method.
    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)
    #     # form.base_fields['total_price'].disabled = True # No longer needed if in readonly_fields
    #     return form