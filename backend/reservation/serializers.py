from rest_framework import serializers
from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        # Campos que el usuario puede enviar y que quieres serializar para la respuesta
        fields = [
            'guest_first_name', 'guest_last_name', 'guest_email', 'guest_phone',
            'check_in_date', 'check_out_date', 'num_adults', 'num_children',
            'special_requests',
            # Los siguientes campos serán calculados o gestionados por el backend
            # 'total_guests', 'daily_rate', 'total_price', 'payment_status', 'status'
        ]
        # Campos que son de solo lectura si quieres devolverlos pero no permites que el cliente los envíe
        read_only_fields = ['total_guests', 'daily_rate', 'total_price', 'payment_status', 'status', 'reservation_date', 'last_updated', 'payment_transaction_id', 'deposit_amount', 'is_email_verified']

    def validate(self, data):
        # Replicar algunas de tus validaciones de clean() del modelo aquí para respuestas más rápidas
        # O, si confías completamente en el clean() del modelo, puedes omitirlas aquí
        if data['check_out_date'] <= data['check_in_date']:
            raise serializers.ValidationError({"check_out_date": "Check-out date must be after check-in date."})

        # if data['check_in_date'] < timezone.localdate(): # Use localdate for comparison
        #     raise serializers.ValidationError({"check_in_date": _("Check-in date cannot be in the past.")})

        if data['num_adults'] < 1:
            raise serializers.ValidationError({"num_adults": "There must be at least one adult in the reservation."})

        # Aquí es donde podrías llamar a la lógica de disponibilidad
        # Esto es una simplificación; en un caso real, necesitarías fechas y tal vez el ID de la instancia
        # para verificar la disponibilidad en el momento de la validación del serializer.
        # Por ahora, asumimos que la disponibilidad se verifica en el método save del modelo
        # o en la vista.
        return data

    def create(self, validated_data):
        # Aquí podrías calcular daily_rate y total_price antes de guardar,
        # o delegar en el método save del modelo si ya lo hace
        # Ejemplo: Asignar una tarifa diaria fija o de un sistema de precios
        validated_data['daily_rate'] = 150.00 # Ejemplo, reemplazar con lógica real
        validated_data['total_price'] = 150
        validated_data['total_guests'] = 1
        # El total_price y total_guests se calcularán en el método save del modelo
        return super().create(validated_data)