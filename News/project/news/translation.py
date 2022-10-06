from modeltranslation.translator import register, TranslationOptions
from .models import Post, Category


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name_of_category', )


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'post_text')
