from django.contrib import admin
from .models import BaseData, PhoneNumber


class PhoneNumberInline(admin.TabularInline):
    model = PhoneNumber
    extra = 1  # Muestra un campo extra vacío para añadir fácilmente
    fields = ["number", "description"]


# Register your models here.
@admin.register(BaseData)
class BaseDataAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("name",)
    ordering = ("name",)
    inlines = [PhoneNumberInline]
