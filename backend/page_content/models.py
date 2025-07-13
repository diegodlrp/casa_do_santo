from django.db import models


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class PageContent(models.Model):
    title = models.CharField(max_length=150)
    excerpt = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to="img", null=True, blank=True)
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, null=True, blank=True)

    def __str__(self):
        return self.slug
