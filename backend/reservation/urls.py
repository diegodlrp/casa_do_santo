# reservations_app/urls.py
from django.urls import path
from .views import AvailableDatesAPIView # Import the new view

urlpatterns = [
    path('available-dates/', AvailableDatesAPIView.as_view(), name='available-dates'), # New endpoint
]