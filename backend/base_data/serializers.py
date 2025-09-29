from rest_framework import serializers
from .models import BaseData


class BaseDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseData
        fields = [
            "name",
            "email",
            "phone",
            "phone2",
            "phone3",
            "address",
            "address_link",
            "logo",
        ]
