from django import forms
from .models import Post, Category


class NewsForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = [
            'title',
            'post_text',
            'category',
        ]


class ArticleForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = [
            'title',
            'post_text',
            'category',
        ]
