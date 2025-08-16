from django.contrib import admin
from .models import BaseData

# Register your models here.
@admin.register(BaseData)
class BaseDataAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("name",)
    ordering = ("name",)