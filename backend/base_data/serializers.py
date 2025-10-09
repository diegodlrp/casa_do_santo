from rest_framework import serializers
from .models import BaseData

from rest_framework import serializers
from .models import BaseData, PhoneNumber

# Serializer para los teléfonos (Paso 1)
class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ["number", "description"] 


# Serializer Corregido para BaseData (Paso 2)
class BaseDataSerializer(serializers.ModelSerializer):

    phones = PhoneNumberSerializer(many=True, read_only=True)
    
    class Meta:
        model = BaseData
        fields = [
            "name",
            "email",
            "phones",
            "address",
            "address_link",
            "logo",
        ]
