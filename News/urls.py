from django.urls import path, include
from django.views.decorators.cache import cache_page
from .views import (
    PostDetail, PostList, PostFilterList, PostCreate, PostEdit, PostDelete,
    ProfileView, upgrade_me, PostCategoryList, subscribe, Index
)

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('', cache_page(60)(PostList.as_view()), name='post_list'),
    path('search/', PostFilterList.as_view(), name='post_search'),
    path('<int:pk>', cache_page(300)(PostDetail.as_view()), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/upgrade/', upgrade_me, name='upgrade'),
    path('categories/<int:pk>', PostCategoryList.as_view(), name='categories'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('hello_world', Index.as_view(), name='hello_world')
]
