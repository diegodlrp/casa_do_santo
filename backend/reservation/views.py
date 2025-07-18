# your_app_name/views.py

from .models import Reservation
from .serializers import ReservationSerializer
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
import datetime

# Create your views here.
class ReservationViewSet(ModelViewSet):
    """
    API endpoint that allows Tags to be viewed or edited.
    """
    queryset = Reservation.objects.all().order_by("id")
    serializer_class = ReservationSerializer
# class ReservationCreateView(generics.CreateAPIView):
#     queryset = Reservation.objects.all()
#     serializer_class = ReservationSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     # Replicar la lógica de disponibilidad aquí o en el serializer's validate method
    #     # Es crucial verificar la disponibilidad antes de guardar
    #     check_in = serializer.validated_data['check_in_date']
    #     check_out = serializer.validated_data['check_out_date']

    #     # Crear una instancia temporal para usar el método is_house_available
    #     temp_reservation = Reservation(
    #         check_in_date=check_in,
    #         check_out_date=check_out
    #     )

    #     if not temp_reservation.is_house_available(check_in, check_out):
    #         return Response(
    #             {"detail": "The house is not available for the selected dates."},
    #             status=status.HTTP_409_CONFLICT # 409 Conflict is good for resource conflicts
    #         )

    #     # Si está disponible, guardar la reserva
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# Puedes añadir una vista para obtener reservas existentes si la necesitas
# class ReservationListView(generics.ListAPIView):
#     queryset = Reservation.objects.all()
#     serializer_class = ReservationSerializer