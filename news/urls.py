from django.urls import path
from .views import ListNews,DetailNews


urlpatterns = [
    path('', ListNews.as_view(), name='posts'),
    path('<int:pk>', DetailNews.as_view(),name='news_detail'),
]