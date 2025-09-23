from django.contrib import admin
from .models import EmailTemplate


# Register your models here.
@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ("slug",)
    search_fields = ("slug",)
    list_filter = ("slug",)
    ordering = ("slug",)


