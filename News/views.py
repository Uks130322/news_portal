from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import PostForm
from .models import Post
from .filters import PostFilter


class PostList(ListView):
    """Show all news, 10 by page. Paginator is in default.html"""

    model = Post
    ordering = '-add_date'
    template_name = 'news.html'
    context_object_name = 'page_list'
    paginate_by = 10
    extra_context = {'posts': Post.objects.all()}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        page = context['page_obj']
        context['paginator_range'] = page.paginator.get_elided_page_range(page.number, on_each_side=1, on_ends=1)
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostFilterList(ListView):
    model = Post
    ordering = '-add_date'
    context_object_name = 'posts'
    paginate_by = 10
    template_name = 'search.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        page = context['page_obj']
        context['paginator_range'] = page.paginator.get_elided_page_range(page.number, on_each_side=1, on_ends=1)
        context['filterset'] = self.filterset
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'create_or_edit.html'
    success_url = '/news/'

    def form_valid(self, form):
        """Create article or news depending on the path"""
        post = form.save(commit=False)
        if self.request.path == '/articles/create/':
            post.type = 'AR'
        post.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Get correct html-title and title on page depending on the path"""
        context = super().get_context_data(**kwargs)
        context['get_title'] = self.get_type()['title']
        context['get_type'] = self.get_type()['content']
        return context

    def get_type(self):
        if self.request.path == '/articles/create/':
            return {'title': 'Create article', 'content': 'Добавить статью'}
        else:
            return {'title': 'Create news', 'content': 'Добавить новость'}


class PostEdit(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'create_or_edit.html'

    def get_context_data(self, **kwargs):
        """Get correct html-title and title on page depending on the path"""
        context = super().get_context_data(**kwargs)
        context['get_title'] = self.get_type()['title']
        context['get_type'] = self.get_type()['content']
        return context

    def get_type(self):
        if 'articles' in self.request.path:
            return {'title': 'Edit article', 'content': 'Редактировать статью'}
        else:
            return {'title': 'Edit news', 'content': 'Редактировать новость'}


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('post_list')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'
