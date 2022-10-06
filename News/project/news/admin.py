from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'post_text', 'date_and_time_of_creation_post']
    list_filter = ['date_and_time_of_creation_post', 'title']
    search_fields = ['title']


class CategoryAdmin(TranslationAdmin):
    model = Category


class TrPostAdmin(TranslationAdmin):
    model = Post


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
