from django.contrib import admin
from .models import EmailTemplate


# Register your models here.
@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("name",)
    ordering = ("name",)
