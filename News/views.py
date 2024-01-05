from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Post


class PostList(ListView):
    """
    Show all news, 10 by page.
    Paginator is in default.html
    """

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

    # def adjusted_elided_pages(self):
    #     return self.paginator_class.get_elided_page_range(on_each_side=1, on_ends=1)
    #
    # def ellipsis(self):
    #     return self.paginator_class.ELLIPSIS


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


# def listing(request, page):
#     posts = Post.objects.all().order_by('-add_date')
#     paginator = Paginator(posts, per_page=10)
#     page_object = paginator.get_page(page)
#     page_object.adjusted_elided_pages = paginator.get_elided_page_range(page, on_each_side=1, on_ends=1)
#     context = {'page_obj': page_object, 'posts': posts}
#     return render(request, 'news.html', context)
