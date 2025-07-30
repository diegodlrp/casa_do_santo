from django.urls import path
from .views import send_mail_view

urlpatterns = [
    path("send-mail/", send_mail_view, name="send-mail"),
]