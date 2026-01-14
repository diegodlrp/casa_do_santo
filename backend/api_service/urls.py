from django.urls import path
from .views import send_mail_view, send_reservation_mail_view

urlpatterns = [
    path("send-mail/", send_mail_view, name="send-mail"),
    path(
        "send-reservationmail/", send_reservation_mail_view, name="send-reservationmail"
    ),
]
