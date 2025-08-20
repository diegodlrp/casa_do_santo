from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Reservation, Guest, DailyPrice  # Ensure Guest is imported
from django.utils.safestring import mark_safe
from calendar import monthrange
import datetime
from urllib.parse import urlencode
from django.urls import reverse, path
from .forms import BulkPriceForm
from django.shortcuts import render, redirect
from django.contrib import messages

# Register your models here.
@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ("name", "last_name", "email", "phone", "vat")
    search_fields = ("name", "last_name", "email", "phone", "vat")
    list_filter = ("name", "last_name")  # Basic filters
    ordering = ("last_name", "name")  # Consistent with model Meta


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "main_guest",  # Displays the __str__ of the Guest object
        "check_in_date",
        "check_out_date",
        "status",
        "total_guests",
        "daily_rate",
        "total_price",
        "payment_status",
        "is_email_verified",
        "get_other_guests_count",  # Custom method for list_display
    )
    list_filter = ("status", "check_in_date", "check_out_date", "payment_status")

    # IMPORTANT: For ForeignKey and ManyToMany fields in search_fields,
    # you need to use the double underscore (__) to traverse relationships.
    search_fields = (
        "main_guest__name",  # Search by main guest's first name
        "main_guest__last_name",  # Search by main guest's last name
        "main_guest__email",  # Search by main guest's email
        "payment_transaction_id",  # Your existing field
        "special_requests",  # Often useful to search here too
    )

    # Fields that should not be editable in the admin form
    readonly_fields = (
        "reservation_date",
        "last_updated",
        "total_guests",  # Calculated in model's clean/save
        "total_price",  # Calculated in model's clean/save
    )

    # `filter_horizontal` is great for ManyToMany fields for better UX
    filter_horizontal = ("other_guests",)  # Use the correct plural name

    fieldsets = (
        (
            _("Guest Details"),
            {"fields": ("main_guest", "other_guests")},  # Use the correct plural name
        ),
        (
            _("Reservation Details"),
            {
                "fields": (
                    "check_in_date",
                    "check_out_date",
                    "num_adults",
                    "num_children",
                    "special_requests",
                )
            },
        ),
        (
            _("Pricing & Payment"),
            {
                "fields": (
                    "daily_rate",
                    "payment_status",
                    "deposit_amount",
                    "payment_transaction_id",
                )
                # total_price is now in readonly_fields, so remove it from here
            },
        ),
        (
            _("Status & Timestamps"),
            {
                "fields": (
                    "status",
                    "reservation_date",
                    "last_updated",
                    "total_guests",
                    "total_price",
                )
                # total_guests and total_price are in readonly_fields, but still need to be listed here
                # if you want them to appear in this fieldset.
            },
        ),
    )

    # --- Custom Methods for Admin List Display ---
    def get_other_guests_count(self, obj):
        return obj.num_adults + obj.num_children

    get_other_guests_count.short_description = _("Other Guests Count")
    get_other_guests_count.admin_order_field = (
        "other_guests__count"  # Allows sorting by count (requires Django 2.0+)
    )

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

@admin.register(DailyPrice)
class DailyPriceAdmin(admin.ModelAdmin):
    list_display = ("date", "price")
    change_list_template = "dailyprices_changelist.html"


    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("bulk-add/", self.admin_site.admin_view(self.bulk_add_view), name="dailyprice_bulk_add"),
        ]
        return custom_urls + urls

    def bulk_add_view(self, request):
        if request.method == "POST":
            form = BulkPriceForm(request.POST)
            if form.is_valid():
                start = form.cleaned_data["start_date"]
                end = form.cleaned_data["end_date"]
                price = form.cleaned_data["price"]

                current = start
                created = 0
                while current <= end:
                    obj, made = DailyPrice.objects.get_or_create(
                        date=current, defaults={"price": price}
                    )
                    if not made:  # already exists → update
                        obj.price = price
                        obj.save()
                    created += 1
                    current += datetime.timedelta(days=1)

                messages.success(request, f"{created} daily prices set from {start} to {end}")
                return redirect("admin:reservation_dailyprice_changelist")
        else:
            form = BulkPriceForm()

        return render(request, "bulk_price_form.html", {
            "form": form,
            "opts": self.model._meta,
        })

    def changelist_view(self, request, extra_context=None):
        today = datetime.date.today()
        
        try:
            year = int(request.GET.get("year", today.year))
        except (TypeError, ValueError):
            year = today.year
        try:
            month = int(request.GET.get("month", today.month))
        except (TypeError, ValueError):
            month = today.month

        cleaned = request.GET.copy()
        cleaned.pop("year", None)
        cleaned.pop("month", None)
        request.GET = cleaned 

        first_weekday, num_days = monthrange(year, month)  # 0=Mon ... 6=Sun
        first_of_month = datetime.date(year, month, 1)
        prev_month = (first_of_month - datetime.timedelta(days=1)).replace(day=1)
        next_month = (first_of_month + datetime.timedelta(days=num_days)).replace(day=1)

        prices = DailyPrice.objects.filter(date__year=year, date__month=month)
        by_day = {p.date.day: p for p in prices}

        changelist_url = reverse("admin:reservation_dailyprice_changelist")
        prev_url = f"{changelist_url}?year={prev_month.year}&month={prev_month.month}"
        next_url = f"{changelist_url}?year={next_month.year}&month={next_month.month}"
        change_url_for = lambda pk: reverse("admin:reservation_dailyprice_change", args=[pk])
        add_url_base = reverse("admin:reservation_dailyprice_add")

        headers = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        parts = ['<table class="calendar">']
        parts.append("<tr>" + "".join(f"<th>{h}</th>" for h in headers) + "</tr><tr>")
        parts.append('<td class="blank-td"></td>' * first_weekday)  # leading blanks

        for d in range(1, num_days + 1):
            obj = by_day.get(d)
            if obj:
                cell = f"<strong>{d}</strong><br><br><a href='{change_url_for(obj.pk)}' class='price-a'>{obj.price} €</a>"
            else:
                if month >= today.month:
                    cell = f"<strong>{d}</strong><br><br><a href='{add_url_base}?date={year}-{month:02d}-{d:02d}' class='price-a'>+</a>"
                else:
                    cell = f"<strong>{d}</strong><br><br>"
            parts.append(f"<td>{cell}</td>")
            if (first_weekday + d) % 7 == 0:
                parts.append("</tr><tr>")
        parts.append("</tr></table><br><br>")
        calendar_html = mark_safe("".join(parts))

        response = super().changelist_view(request, extra_context=extra_context)
        if hasattr(response, "context_data"):
            ctx = response.context_data
            ctx["calendar"] = calendar_html
            ctx["year"] = year
            ctx["month"] = month
            ctx["prev_url"] = prev_url
            ctx["next_url"] = next_url
        return response


    # def get_urls(self):
    #     urls = super().get_urls()
    #     custom_urls = [
    #         path("calendar/", self.admin_site.admin_view(self.calendar_view), name="dailyprice_calendar"),
    #     ]
    #     return custom_urls + urls

    # def calendar_view(self, request):
    #     today = datetime.date.today()
    #     year, month = today.year, today.month

    #     # get all prices for the current month
    #     first_day, num_days = monthrange(year, month)
    #     days = DailyPrice.objects.filter(date__year=year, date__month=month)

    #     price_map = {d.date.day: d.price for d in days}

    #     # build calendar HTML
    #     calendar_html = "<table class='calendar'>"
    #     calendar_html += "<tr>" + "".join(f"<th>{d}</th>" for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]) + "</tr><tr>"

    #     # empty cells before first day
    #     calendar_html += "<td></td>" * ((first_day + 6) % 7)

    #     # fill days
    #     for day in range(1, num_days + 1):
    #         price = price_map.get(day, "-")
    #         calendar_html += f"<td>{day}<br>{price}</td>"
    #         if (day + first_day) % 7 == 0:
    #             calendar_html += "</tr><tr>"

    #     calendar_html += "</tr></table>"

    #     from django.shortcuts import render
    #     return render(request, "admin/dailyprice_calendar.html", {
    #         "calendar": mark_safe(calendar_html),
    #         "opts": self.model._meta,
    #     })