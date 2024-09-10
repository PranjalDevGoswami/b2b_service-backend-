from django.shortcuts import render
from api.account.permissions import IsSuperUser, HasRolePermission

# Create your views here.
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.db.models import Q

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
    

class InterviewDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        user = request.user
        
        # Fetch the UserRole instance for this user
        user_role = UserRole.objects.filter(user=user).first()
        if not user_role:
            return Response({'error': 'User role not found'}, status=400)
        
        # Fetch related interviews
        interviews = Interview.objects.filter(user=user)
        interview_data = []
        
        for interview in interviews:
            interview_serializer = InterviewSerializer(interview)
            interview_dict = interview_serializer.data
            interview_dict['questions'] = []
            
            # Fetch survey questions by panels related to the user's role
            panels = CreatePanel.objects.filter(users=user_role)
            survey_questions = SurveyQuestion.objects.filter(panels__in=panels).distinct()  # Ensuring unique survey questions
            
            question_ids_added = set()  # To track already added questions
            
            for question in survey_questions:
                if question.id not in question_ids_added:
                    question_serializer = SurveyQuestionSerializer(question)
                    question_data = question_serializer.data
                    question_data['answers'] = []
                    
                    # Fetch survey answers provided by the user for this question
                    survey_answers = SurveyAnswer.objects.filter(user=user, question=question).distinct()
                    
                    answer_ids_added = set()  # To track already added answers
                    
                    for answer in survey_answers:
                        if answer.id not in answer_ids_added:
                            answer_serializer = SurveyAnswerSerializer(answer)
                            answer_data = answer_serializer.data
                            
                            # Fetch reward points related to this answer
                            reward = Reward.objects.filter(user=user).first()
                            answer_data['reward_points'] = reward.points if reward else 0
                            
                            question_data['answers'].append(answer_data)
                            answer_ids_added.add(answer.id)
                    
                    interview_dict['questions'].append(question_data)
                    question_ids_added.add(question.id)
            
            interview_data.append(interview_dict)
        
        return Response({
            'interviews': interview_data
        })
        
        
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

