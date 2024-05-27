from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from api.account import views

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),  
    path('register/', B2bUserRegistration.as_view(), name='register'),
    path('login/', B2BUserLogin.as_view(),name="user-login"),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('reset-password/<int:uid>/<token>/', PasswordResetView.as_view(), name='password_reset'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('logout/', Logout.as_view(), name='logout'),
]
