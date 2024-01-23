from django import forms
from django_filters import FilterSet, ModelChoiceFilter, DateFilter, CharFilter
from .models import Post, Author, Category


class PostFilter(FilterSet):
    # category = ModelChoiceFilter(
    #     queryset=Category.objects.all(),
    #     lookup_expr='exact',
    #     label='Категория',
    #     empty_label='Все категории',
    # )

    title = CharFilter(
        label='Содержит',
        lookup_expr='icontains'
    )
    author = ModelChoiceFilter(
        queryset=Author.objects.all(),
        lookup_expr='exact',
        label='Автор',
        empty_label='Все авторы',
    )
    add_date = DateFilter(
        label='Опубликованы после',
        lookup_expr='gt',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form'})
    )

    class Meta:
        model = Post
        fields = []
