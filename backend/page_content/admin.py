from django.contrib import admin
from .models import Tag, PageContent, Image


# Register your models here.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("name",)
    ordering = ("name",)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("caption", "image_file")
    search_fields = ("caption", "image_file")
    list_filter = ("caption", "image_file")
    ordering = ("-sort_order", "caption", "image_file")


@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display = ("slug", "title")
    search_fields = ("slug", "title")
    list_filter = ("tags",)
    ordering = ("-sort_order", "slug", "title")
