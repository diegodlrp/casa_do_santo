from modeltranslation.translator import register, TranslationOptions
from .models import EmailTemplate


@register(EmailTemplate)
class ProductTranslationOptions(TranslationOptions):
    fields = ("excerpt", "content")  # Fields to be translated
