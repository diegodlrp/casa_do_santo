from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class BaseData(models.Model):
    name = models.CharField(max_length=20,verbose_name=_("Name"))
    email = models.EmailField(
        verbose_name=_("Email"), blank=True
    )
    phone = models.CharField(max_length=9, verbose_name=_("Phone"))
    address = models.CharField(max_length=200, verbose_name=_("Address"))
    address_link = models.CharField(max_length=200, verbose_name=_("Address Link"))