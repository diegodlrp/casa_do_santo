from rest_framework import serializers
from .models import PageContent, Tag, Image


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["caption", "image_file"]


class PageContentSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    gallery_images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = PageContent
        fields = [
            "title",
            "excerpt",
            "gallery_images",
            "image",
            "date",
            "slug",
            "content",
            "tags",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.featured_image and obj.featured_image.image_file:
            return request.build_absolute_uri(obj.featured_image.image_file.url)
        return None

