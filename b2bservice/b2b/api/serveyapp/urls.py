
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    LanguageViewSet, SurveyViewSet, SurveyQuestionDetailViewSet, SurveyAnswerViewSet, 
    InterviewViewSet, MissedInterviewViewSet, RewardViewSet, CommunityViewSet, 
    CommunityMemberViewSet, CommunityPostViewSet, CommunityCommentViewSet, CommunityLikeViewSet
)

router = DefaultRouter()
router.register(r'languages', LanguageViewSet)
router.register(r'surveys', SurveyViewSet)
router.register(r'survey-question-details', SurveyQuestionDetailViewSet)
router.register(r'survey-answers', SurveyAnswerViewSet)
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
