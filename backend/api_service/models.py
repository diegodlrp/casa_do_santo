from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class EmailTemplate(models.Model):
    slug = models.SlugField(unique=True, db_index=True, verbose_name=_("Slug"))
    excerpt = models.CharField(
        max_length=200, null=True, blank=True, verbose_name=_("Asunto")
    )
    content = models.TextField(null=True, blank=True, verbose_name=_("Contenido"))

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = _("Plantilla Correo")
        verbose_name_plural = _("Plantillas Correos")
