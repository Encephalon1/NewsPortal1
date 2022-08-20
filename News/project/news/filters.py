from django.forms import DateTimeInput
from django_filters import FilterSet, DateTimeFilter
from .models import Post


class PostFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='date_and_time_of_creation_post',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%d.%m.%Y %H:%M',
            attrs={'type': 'datetime-local'}
        )
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'category': ['exact']
        }
