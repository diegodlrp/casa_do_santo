from rest_framework import serializers
from .models import BaseData


class BaseDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseData
        fields = ["name", "email", "phone", "address", "address_link", "logo"]
