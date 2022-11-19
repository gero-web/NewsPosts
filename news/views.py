import logging

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import Post, SubscriptionCategory, Category, Author
from .form import NewsAndPostForms
from .filter import PostFilter
from django.core.cache import cache


@login_required
def Sucrabe(req, pk):
    user = req.user
    cate = Category.objects.get(pk=pk)
    sub = SubscriptionCategory(category=cate, user=user)
    sub.save()
    return HttpResponseRedirect("/news")


class ListPost(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts.html'
    ordering = '-created'
    queryset = Post.objects.filter(choise='ar')
    paginate_by = 10


class Index(TemplateView):

    template_name = 'index.html'


class ListNews(ListView):

    model = Post
    context_object_name = 'posts'
    template_name = 'news.html'
    ordering = '-created'
    queryset = Post.objects.filter(choise='nw')
    paginate_by = 2

    def get_queryset(self):

        queryset = super().get_queryset()
        self.filter_queryset = PostFilter(self.request.GET, queryset)
        return self.filter_queryset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filter_queryset

        context['category'] = Category.objects.all()
        return context


class DetailNews(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'detail_posts.html'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'detail_news-{self.kwargs["pk"]}', None)

        if obj is None:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'detail_news-{self.kwargs["pk"]}', obj, timeout=60 * 5)

        return obj


class CreatePost(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = NewsAndPostForms
    template_name = 'create.html'
    success_url = reverse_lazy('posts')
    model = Post

    def form_valid(self, form):
        if form.is_valid():
            article: Post = form.save(commit=False)
            article.choise = 'ar'
        return super().form_valid(form)


class CreateNews(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = NewsAndPostForms
    template_name = 'create.html'
    success_url = reverse_lazy('news')
    model = Post

    def form_valid(self, form):
        if form.is_valid():
            post: Post = form.save(commit=False)
        return super().form_valid(form)


class DeletePostOrNews(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'confirm.html'
    success_url = reverse_lazy('news')


class EditPostOrNews(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    model = Post
    form_class = NewsAndPostForms
    template_name = 'edit.html'
