from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView, ListView
from django.views.generic import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import Post
from .form import NewsAndPostForms
from .filter import PostFilter


class ListPost(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts.html'
    ordering = '-created'
    queryset = Post.objects.filter(choise='ar')
    paginate_by = 10


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
        return context


class DetailNews(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'detail_posts.html'


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


class DeletePostOrNews(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'confirm.html'


class EditPostOrNews(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    model = Post
    form_class = NewsAndPostForms
    template_name = 'edit.html'
