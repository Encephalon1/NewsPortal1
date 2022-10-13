from rest_framework import serializers
from .models import *


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'post_text', 'rating_of_post', 'date_and_time_of_creation_post',
                  'post_author', 'category', 'post_type']
