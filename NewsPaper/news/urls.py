from django.urls import path
from .views import PostsList, PostDetail, PostSearch, upgrade_me, subscribe_to_categories, unsubscribe_from_categories, \
    set_timezone

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('category/subscribe/', subscribe_to_categories, name='subscribe_to_categories'),
    path('category/unsubscribe/', unsubscribe_from_categories, name='unsubscribe_from_categories'),
    path('set-tz/', set_timezone, name='set_timezone')
]
