from django.shortcuts import render
from django.views.generic import DetailView,ListView
from .models import  Post

class ListNews(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts.html'
    ordering = '-created'


class DetailNews(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'detail_posts.html'



