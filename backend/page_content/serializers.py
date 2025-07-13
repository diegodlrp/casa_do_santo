from rest_framework import serializers
from .models import PageContent, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

class PageContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageContent
        fields = ["title","excerpt","image","date","slug","content", "tags", ]