from django.urls import path
from .views import ListNews, DetailNews, DeletePostOrNews, ListPost, Sucrabe
from .views import CreateNews, CreatePost, EditPostOrNews
from django.views.decorators.cache import cache_page

urlpatterns = [


    path('<int:pk>', DetailNews.as_view(), name='news_detail'),

    path('sub/<int:pk>', Sucrabe, name='sub'),
    path('articles/', ListPost.as_view(), name='posts'),
    path('articles/create/', CreatePost.as_view(), name='create_post'),
    path('articles/<int:pk>/edit', EditPostOrNews.as_view(), name='edit_post'),
    path('articles/<int:pk>/delete', DeletePostOrNews.as_view(), name='delete_article'),
    path('news/', ListNews.as_view(), name='news'),
    path('news/create/', CreateNews.as_view(), name='create_news'),
    path('news/<int:pk>/edit', EditPostOrNews.as_view(), name='edit_news'),
    path('news/<int:pk>/delete', DeletePostOrNews.as_view(), name='delete_news'),
]
