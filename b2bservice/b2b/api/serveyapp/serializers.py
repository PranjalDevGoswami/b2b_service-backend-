from rest_framework import serializers
from .models import (
    Language, Survey, servey_question_detail, SurveyAnswer, Interview, 
    MissedInterview, Reward, Community, CommunityMember, CommunityPost, 
    CommunityComment, CommunityLike
)
from django.contrib.auth import get_user_model

User = get_user_model()

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name']

class SurveySerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Survey
        fields = ['id', 'question', 'points', 'created_by', 'industry', 'created_at']

class SurveyQuestionDetailSerializer(serializers.ModelSerializer):
    survey = SurveySerializer(read_only=True)

    class Meta:
        model = servey_question_detail
        fields = ['id', 'survey', 'title', 'company', 'language', 'descriptions', 'start_date', 'end_date', 'is_active', 'time_zone', 'no_of_questions', 'created_at']

class SurveyAnswerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    survey = SurveySerializer(read_only=True)

    class Meta:
        model = SurveyAnswer
        fields = ['id', 'user', 'survey', 'answer', 'is_public', 'created_at']

class InterviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Interview
        fields = ['id', 'user', 'title', 'date', 'duration', 'completed', 'voucher']

class MissedInterviewSerializer(serializers.ModelSerializer):
    interview = InterviewSerializer(read_only=True)

    class Meta:
        model = MissedInterview
        fields = ['id', 'interview', 'missed_at']

class RewardSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Reward
        fields = ['id', 'user', 'points', 'description', 'created_at']

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['id', 'name', 'description', 'created_at']

class CommunityMemberSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    community = CommunitySerializer(read_only=True)

    class Meta:
        model = CommunityMember
        fields = ['id', 'user', 'community', 'joined_at']

class CommunityPostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    community = CommunitySerializer(read_only=True)

    class Meta:
        model = CommunityPost
        fields = ['id', 'community', 'user', 'content', 'created_at']

class CommunityCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    post = CommunityPostSerializer(read_only=True)

    class Meta:
        model = CommunityComment
        fields = ['id', 'post', 'user', 'comment', 'created_at']

class CommunityLikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    post = CommunityPostSerializer(read_only=True)

    class Meta:
        model = CommunityLike
        fields = ['id', 'user', 'post', 'created_at']
