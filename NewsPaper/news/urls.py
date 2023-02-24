from django.urls import path
from .views import PostsList, PostDetail, PostSearch, upgrade_me

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('upgrade/', upgrade_me, name='upgrade')
]
