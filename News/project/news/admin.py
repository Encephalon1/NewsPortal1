from django.contrib import admin
from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'post_text', 'date_and_time_of_creation_post']
    list_filter = ['date_and_time_of_creation_post', 'title']
    search_fields = ['title']


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
