from django.db import models
from django.utils.translation import gettext_lazy as _


class PhoneNumber(models.Model):
    # Clave foránea al modelo BaseData.
    # Cada número de teléfono se relaciona con UNA BaseData.
    base_data = models.ForeignKey(
        "BaseData",
        on_delete=models.CASCADE,
        related_name="phones",  # Este es el nombre que usarás para acceder a los teléfonos desde BaseData
        verbose_name=_("Base Data"),
    )

    number = models.CharField(max_length=15, verbose_name=_("Phone Number"))
    description = models.CharField(
        max_length=50,
        verbose_name=_("Description (e.g., Main, Office, Mobile)"),
        blank=True,
    )

    min_nights = models.PositiveIntegerField(default=3)


    class Meta:
        verbose_name = _("Teléfono")
        verbose_name_plural = _("Teléfonos")

    def __str__(self):
        return f"{self.number} ({self.base_data.name})"


# Create your models here.
class BaseData(models.Model):
    name = models.CharField(max_length=20, verbose_name=_("Name"))
    email = models.EmailField(verbose_name=_("Email"), blank=True)
    email_app_password = models.CharField(
        max_length=200, verbose_name=_("Contraseña aplicacion email"), blank=True
    )

    address = models.CharField(max_length=200, verbose_name=_("Address"))
    address_link = models.CharField(max_length=200, verbose_name=_("Address Link"))
    logo = models.image_file = models.ImageField(
        upload_to="gallery_images/",  # Las imágenes se guardarán en MEDIA_ROOT/gallery_images/
        verbose_name=_("Image File"),
        null=True,
        blank=True,
    )
