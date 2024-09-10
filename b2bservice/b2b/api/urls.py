from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApiStatus

urlpatterns = [
    path('', ApiStatus, name='status-ok'),
    path('account/', include('api.account.urls')),
    path('project/', include('api.projectapp.urls')),
    path('feed/', include('api.feeds.urls')),
]