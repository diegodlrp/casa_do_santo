from django.shortcuts import render
from .serializers import BaseDataSerializer
from .models import BaseData
from rest_framework.viewsets import ModelViewSet

# Create your views here.
class BaseDataViewSet(ModelViewSet):
    """
    API endpoint that allows BaseData to be viewed or edited.
    """

    queryset = BaseData.objects.all().order_by("id")
    serializer_class = BaseDataSerializer
