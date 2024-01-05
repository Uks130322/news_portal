from django_filters import FilterSet, ModelChoiceFilter
from .models import Post, Author


class PostFilter(FilterSet):
    author = ModelChoiceFilter(
        'author__user__username',
        queryset=Author.user.username.objects.all(),
        label='Автор',
        empty_label='Все авторы'
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'add_date': ['gt']
        }