from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class BaseData(models.Model):
    name = models.CharField(max_length=20, verbose_name=_("Name"))
    email = models.EmailField(verbose_name=_("Email"), blank=True)
    email_app_password = models.CharField(
        max_length=200, verbose_name=_("Contraseña aplicacion email"), blank=True
    )
    phone = models.CharField(max_length=15, verbose_name=_("Phone"))
    phone2 = models.CharField(max_length=15, verbose_name=_("Phone2"), blank=True)
    phone3 = models.CharField(max_length=15, verbose_name=_("Phone3"), blank=True)
    address = models.CharField(max_length=200, verbose_name=_("Address"))
    address_link = models.CharField(max_length=200, verbose_name=_("Address Link"))
    logo = models.image_file = models.ImageField(
        upload_to="gallery_images/",  # Las imágenes se guardarán en MEDIA_ROOT/gallery_images/
        verbose_name=_("Image File"),
        null=True,
        blank=True,
    )
