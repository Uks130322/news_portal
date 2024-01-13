from django.urls import path
from .views import (
    PostDetail, PostList, PostFilterList, PostCreate, PostEdit, PostDelete, ProfileView
)

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('search/', PostFilterList.as_view(), name='post_search'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('profile/', ProfileView.as_view(), name='profile')
]