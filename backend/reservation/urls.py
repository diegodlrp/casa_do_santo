# reservations_app/urls.py
from django.urls import path
from .views import AvailableDatesAPIView, DailyPriceDataRangesView

urlpatterns = [
    # First path() call for available-dates
    path("available-dates/", AvailableDatesAPIView.as_view(), name="available-dates"),
    # Second, separate path() call for price-data-ranges
    path(
        "price-data-ranges/",
        DailyPriceDataRangesView.as_view(),
        name="price-data-ranges",
    ),
]
