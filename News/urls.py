from django.urls import path
from .views import PostDetail, PostList     # , listing


urlpatterns = [
    path('', PostList.as_view()),
    # path('page=<int:page>', listing, name='news-by-page'),
    path('<int:pk>', PostDetail.as_view()),
]