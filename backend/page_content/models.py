# your_app_name/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _


# --- Modelo Tag (sin cambios) ---
class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name=_("Name"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


# --- Modelo Image (el mismo que hemos definido para la galería) ---
# Este modelo representa cada archivo de imagen individual.
class Image(models.Model):
    image_file = models.ImageField(
        upload_to="gallery_images/",  # Las imágenes se guardarán en MEDIA_ROOT/gallery_images/
        verbose_name=_("Image File"),
    )
    caption = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("Caption")
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Uploaded At"))

    sort_order = models.PositiveIntegerField(default=0)
    hidden = models.BooleanField(default=False,  verbose_name=_("Hidden in Gallery"))
    # Una imagen puede tener múltiples tags (para categorizar imágenes en tu librería)
    # tags = models.ManyToManyField(
    #     Tag,
    #     blank=True,
    #     related_name='images',
    #     verbose_name=_("Tags")
    # )

    def __str__(self):
        return self.caption or self.image_file.name

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")
        ordering = ["-uploaded_at"]


# --- Modelo PageContent (con los dos campos de imagen) ---
class PageContent(models.Model):
    title = models.CharField(max_length=150, verbose_name=_("Title"))
    excerpt = models.CharField(
        max_length=200, null=True, blank=True, verbose_name=_("Excerpt")
    )
    date = models.DateField(auto_now=True, verbose_name=_("Date"))
    slug = models.SlugField(unique=True, db_index=True, verbose_name=_("Slug"))
    content = models.TextField(verbose_name=_("Content"))
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_("Tags"))
    sort_order = models.PositiveIntegerField(default=0)

    # 1. Campo One-to-One para la IMAGEN DESTACADA/PRINCIPAL
    # Cada PageContent puede tener una única imagen destacada.
    # Una imagen solo puede ser la destacada de un PageContent a la vez.
    featured_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,  # Si la imagen se borra, el campo se pone a NULL.
        null=True,  # Permite que un PageContent no tenga imagen destacada.
        blank=True,  # Permite que el campo esté vacío en formularios.
        related_name="featured_on_page",  # Para acceder al PageContent desde la imagen: my_image.featured_on_page
        verbose_name=_("Featured Image"),
    )

    # 2. Campo Many-to-Many para las IMÁGENES DE GALERÍA ADICIONALES
    # Cada PageContent puede tener cero o varias imágenes de galería.
    # Una imagen puede estar en la galería de varios PageContent.
    gallery_images = models.ManyToManyField(
        Image,
        blank=True,
        related_name="pages_in_gallery",  # Para acceder a los PageContent desde la imagen: my_image.pages_in_gallery.all()
        verbose_name=_("Gallery Images"),
    )

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = _("Page Content")
        verbose_name_plural = _("Page Contents")
        ordering = ["-sort_order", "-date", "title"]
