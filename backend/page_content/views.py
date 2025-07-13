from django.shortcuts import render
from .serializers import PageContentSerializer, TagSerializer
from .models import PageContent, Tag
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import translation

# Create your views here.
class TagViewSet(ModelViewSet):
    """
    API endpoint that allows Tags to be viewed or edited.
    """
    queryset = Tag.objects.all().order_by("id")
    serializer_class = TagSerializer
    lookup_field = 'name'

    @action(detail=True, methods=["get"], url_path="page_content")
    def list_pagecontent(self, request,  name=None):
        """
        Retrieves all pagecontent associated with a specific tag.
        """
        try:
            tag = Tag.objects.get(name=name)
        except Tag.DoesNotExist:
            return Response({"detail": "Tag not found."}, status=404)

        tag_id = tag.id
        queryset = PageContent.objects.filter(tags__id=tag_id).order_by("id")
        
        # The serializer_class is fine here, as it's just a reference
        # serializer_class = PageContentSerializer # You already have this imported at the top

        desired_lang = request.query_params.get('lang')

        if desired_lang:
            # Temporarily activate the desired language for this request's context
            with translation.override(desired_lang):
                # Instantiate the serializer *inside* the translation.override block
                serializer = PageContentSerializer(queryset, many=True, context={"request": request})
                return Response(serializer.data)
        else:
            # Fallback to language determined by LocaleMiddleware (Accept-Language, etc.)
            # Instantiate the serializer here as well
            serializer = PageContentSerializer(queryset, many=True, context={"request": request})
            return Response(serializer.data)
        
        

class PageContentViewSet(ModelViewSet):
    """
    Retrieves all pagecontent 
    """
    queryset = PageContent.objects.all().order_by("id")
    serializer_class = PageContentSerializer
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        desired_lang = request.query_params.get('lang')

        if desired_lang:
            with translation.override(desired_lang):
                instance = self.get_object()
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        desired_lang = request.query_params.get('lang')
        print("desired_lang",desired_lang)
        if desired_lang:
            with translation.override(desired_lang):
                queryset = self.filter_queryset(self.get_queryset())
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)
        # Using super().list() is good here if no language override is needed
        return super().list(request, *args, **kwargs)