from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.cache import cache
from .models import Post, Author, Category
from .forms import NewsForm, ArticleForm
from .filters import PostFilter
from .tasks import send_mail


class PostList(ListView):
    model = Post
    ordering = '-date_and_time_of_creation_post'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


class PostDetail(DetailView):
    model = Post
    template_name = 'single_news.html'
    context_object_name = 'single_news'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


def subscribe(request, pk):
    context = {
        'user': request.user,
        'cat': Category.objects.get(id=pk),
        'is_subscribed': Category.objects.get(id=pk).subscribers.filter(id=request.user.id).exists()
    }

    return render(request, 'subscribe.html', context)


# Подписка на группу
@login_required
def add_subscribe(request, pk):
    user = request.user
    cat = Category.objects.get(id=pk)
    is_subscribed = cat.subscribers.filter(id=user.id).exists()
    if not is_subscribed:
        cat.subscribers.add(user)
    return redirect('/news/')


# Отписка от группы
@login_required
def delete_subscribe(request, pk):
    user = request.user
    cat = Category.objects.get(id=pk)
    is_subscribed = cat.subscribers.filter(id=user.id).exists()
    if is_subscribed:
        cat.subscribers.remove(user)
    return redirect('/news/')


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'NW'
        post.post_author = Author.objects.get(author=self.request.user)
        send_mail.delay()
        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    form_class = ArticleForm
    model = Post
    template_name = 'article_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'AR'
        post.post_author = Author.objects.get(author=self.request.user)
        send_mail.delay()
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    permission_required = 'news.change_post'
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'

    def test_func(self):
        post = self.get_object()
        return post.post_author == self.request.user


class ArticleUpdate(PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    permission_required = 'news.change_post'
    form_class = ArticleForm
    model = Post
    template_name = 'article_edit.html'

    def test_func(self):
        post = self.get_object()
        return post.post_author == self.request.user


class NewsDelete(PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    permission_required = 'news.delete_post'
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return post.post_author == self.request.user


class ArticleDelete(PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    permission_required = 'news.delete_post'
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return post.post_author == self.request.user


class SearchNews(ListView):
    model = Post
    template_name = 'search_news.html'
    context_object_name = 'search_news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        # context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs
