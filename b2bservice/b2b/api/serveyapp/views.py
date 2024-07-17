from django.shortcuts import render
from api.account.permissions import IsSuperUser, HasRolePermission

# Create your views here.
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

class SurveyQuestionViewSet(viewsets.ModelViewSet):
    queryset = SurveyQuestion.objects.all()
    serializer_class = SurveyQuestionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return SurveyQuestion.objects.all()
        else:
            return SurveyQuestion.objects.filter(created_by=self.request.user)

class SurveyAnswerViewSet(viewsets.ModelViewSet):
    queryset = SurveyAnswer.objects.all()
    serializer_class = SurveyAnswerSerializer
    permission_classes = [IsAuthenticated]  # 
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return SurveyQuestion.objects.all()
        else:
            return SurveyQuestion.objects.filter(created_by=self.request.user)
        
        user_role = UserRole.objects.filter(user=self.request.user).first()
        
        if user_role and user_role.permissions.filter(codename='view_interview').exists():
            return Interview.objects.filter(created_by=self.request.user)
        
        
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

