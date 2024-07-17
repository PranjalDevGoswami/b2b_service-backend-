
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *
from . import views

router = DefaultRouter()
router.register(r'languages', LanguageViewSet)
router.register(r'survey-questions', views.SurveyQuestionViewSet)
router.register(r'survey-answers', views.SurveyAnswerViewSet)
router.register(r'interviews', InterviewViewSet)
router.register(r'missed-interviews', MissedInterviewViewSet)
router.register(r'rewards', RewardViewSet)
router.register(r'communities', CommunityViewSet)
router.register(r'community-members', CommunityMemberViewSet)
router.register(r'community-posts', CommunityPostViewSet)
router.register(r'community-comments', CommunityCommentViewSet)
router.register(r'community-likes', CommunityLikeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
