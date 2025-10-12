from django.utils import timezone
from .models import ReservationEditToken


def create_one_time_link(request, reservation):
    """
    Genera un token para editar una vez la reserva
    Solo permite modificar la reserva asociada
    """

    # creamos el token
    token, created = ReservationEditToken.objects.get_or_create(reservation=reservation)

    # If the token already existed, we'll refresh it to ensure it's not expired or used.
    # This makes the button "re-send a new link" if one was sent before.
    if not created:
        token.created_at = timezone.now()
        token.used = False
        token.save()

    return token
