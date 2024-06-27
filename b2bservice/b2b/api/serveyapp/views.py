from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import (
    Language, Survey, servey_question_detail, SurveyAnswer, Interview, 
    MissedInterview, Reward, Community, CommunityMember, CommunityPost, 
    CommunityComment, CommunityLike
)
from .serializers import (
    LanguageSerializer, SurveySerializer, SurveyQuestionDetailSerializer, SurveyAnswerSerializer, 
    InterviewSerializer, MissedInterviewSerializer, RewardSerializer, CommunitySerializer, 
    CommunityMemberSerializer, CommunityPostSerializer, CommunityCommentSerializer, CommunityLikeSerializer
)

class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

class SurveyQuestionDetailViewSet(viewsets.ModelViewSet):
    queryset = servey_question_detail.objects.all()
    serializer_class = SurveyQuestionDetailSerializer

class SurveyAnswerViewSet(viewsets.ModelViewSet):
    queryset = SurveyAnswer.objects.all()
    serializer_class = SurveyAnswerSerializer

class InterviewViewSet(viewsets.ModelViewSet):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer

class MissedInterviewViewSet(viewsets.ModelViewSet):
    queryset = MissedInterview.objects.all()
    serializer_class = MissedInterviewSerializer

class RewardViewSet(viewsets.ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer

class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

class CommunityMemberViewSet(viewsets.ModelViewSet):
    queryset = CommunityMember.objects.all()
    serializer_class = CommunityMemberSerializer

class CommunityPostViewSet(viewsets.ModelViewSet):
    queryset = CommunityPost.objects.all()
    serializer_class = CommunityPostSerializer

class CommunityCommentViewSet(viewsets.ModelViewSet):
    queryset = CommunityComment.objects.all()
    serializer_class = CommunityCommentSerializer

class CommunityLikeViewSet(viewsets.ModelViewSet):
    queryset = CommunityLike.objects.all()
    serializer_class = CommunityLikeSerializer
