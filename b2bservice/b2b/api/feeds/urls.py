from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.feeds.views import *

router = DefaultRouter()




urlpatterns = [
    path('', include(router.urls)),
    path('feeds/', FeedList.as_view(), name='feed-list'),
    path('feed/view/', FeedView.as_view(), name='feed-detail'),
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('user/tags/', UserTagSelectionView.as_view(), name='user-tag-selection'),
]
