from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('question', 'points', 'created_by', 'industry', 'created_at')
    search_fields = ('question',)
    list_filter = ('created_at', 'industry')
    raw_id_fields = ('created_by',)

@admin.register(servey_question_detail)
class SurveyQuestionDetailAdmin(admin.ModelAdmin):
    list_display = ('survey', 'title', 'company', 'language', 'start_date', 'end_date', 'is_active', 'created_at')
    search_fields = ('title', 'descriptions')
    list_filter = ('is_active', 'start_date', 'end_date')
    raw_id_fields = ('survey', 'company', 'language')

@admin.register(SurveyAnswer)
class SurveyAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'survey', 'answer', 'is_public', 'created_at')
    search_fields = ('answer',)
    list_filter = ('created_at', 'is_public')
    raw_id_fields = ('user', 'survey')

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'date', 'duration', 'completed', 'voucher')
    search_fields = ('title',)
    list_filter = ('date', 'completed')
    raw_id_fields = ('user',)

@admin.register(MissedInterview)
class MissedInterviewAdmin(admin.ModelAdmin):
    list_display = ('interview', 'missed_at')
    search_fields = ('interview__title',)
    list_filter = ('missed_at',)
    raw_id_fields = ('interview',)

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'description', 'created_at')
    search_fields = ('description',)
    list_filter = ('created_at',)
    raw_id_fields = ('user',)

@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)

@admin.register(CommunityMember)
class CommunityMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'community', 'joined_at')
    search_fields = ('community__name', 'user__username')
    list_filter = ('joined_at',)
    raw_id_fields = ('user', 'community')
    unique_together = ('user', 'community')

@admin.register(CommunityPost)
class CommunityPostAdmin(admin.ModelAdmin):
    list_display = ('community', 'user', 'content', 'created_at')
    search_fields = ('content', 'user__username', 'community__name')
    list_filter = ('created_at',)
    raw_id_fields = ('community', 'user')

@admin.register(CommunityComment)
class CommunityCommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'comment', 'created_at')
    search_fields = ('comment', 'user__username', 'post__content')
    list_filter = ('created_at',)
    raw_id_fields = ('post', 'user')

@admin.register(CommunityLike)
class CommunityLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    search_fields = ('user__username', 'post__content')
    list_filter = ('created_at',)
    raw_id_fields = ('user', 'post')
    unique_together = ('user', 'post')
