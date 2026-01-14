from modeltranslation.translator import register, TranslationOptions
from .models import PageContent


@register(PageContent)
class ProductTranslationOptions(TranslationOptions):
    fields = ("title", "content", "excerpt")  # Fields to be translated
