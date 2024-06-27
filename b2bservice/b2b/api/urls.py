from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ApiStatus

urlpatterns = [
    path('', ApiStatus, name='status-ok'),
    path('account/', include('api.account.urls')),
    path('servey/', include('api.serveyapp.urls')),
]