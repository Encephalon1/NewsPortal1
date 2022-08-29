from django.urls import path
from .views import \
    PostList, PostDetail, NewsCreate, ArticleCreate, NewsUpdate, ArticleUpdate, NewsDelete, ArticleDelete, \
    SearchNews, add_subscribe, delete_subscribe, subscribe


urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_update'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('search/', SearchNews.as_view(), name='filter_news'),
    path('add_subscribe/<int:pk>', add_subscribe, name='add_subscribe'),
    path('delete_subscribe/<int:pk>', delete_subscribe, name='delete_subscribe'),
    path('subscribe/<int:pk>/', subscribe, name='subscribe'),
]
