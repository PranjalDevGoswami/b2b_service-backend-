
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.feeds.views import FeedList, FeedView

router = DefaultRouter()




urlpatterns = [
    path('', include(router.urls)),
   path('feeds/', FeedList.as_view(), name='feed-list'),
   path('feed/view/', FeedView.as_view(), name='feed-detail'),
]
