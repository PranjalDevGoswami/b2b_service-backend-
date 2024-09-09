from django.contrib import admin
from .models import *

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class InterviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'date', 'duration', 'completed', 'voucher')
    search_fields = ('title', 'user__username')

    def has_add_permission(self, request):
        """
        Allow the user 'ankit.sharma@novusinsights.com' to create new Interview instances.
        """
        if request.user.email == 'ankit.sharma@novusinsights.com':
            return True
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        """
        Prevent the user 'ankit.sharma@novusinsights.com' from deleting any Interview instances.
        """
        if request.user.email == 'ankit.sharma@novusinsights.com':
            return False
        return super().has_delete_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        """
        Optionally allow or disallow editing for 'ankit.sharma@novusinsights.com'.
        """
        if request.user.email == 'ankit.sharma@novusinsights.com':
            return True  # Change this to False if you want to restrict editing as well
        return super().has_change_permission(request, obj)

    def has_view_permission(self, request, obj=None):
        """
        Ensure the user 'ankit.sharma@novusinsights.com' can view the Interview model.
        """
        if request.user.email == 'ankit.sharma@novusinsights.com':
            return True
        return super().has_view_permission(request, obj)

admin.site.register(Interview, InterviewAdmin)

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


class CreatePanelAdmin(admin.ModelAdmin):
    # Display these fields in the admin list view
    list_display = ('name', 'display_users', 'created_at', 'updated_at', 'is_active')
    
    # Enable searching by 'name'
    search_fields = ('name',)
    
    # Add filters for these fields
    list_filter = ('is_active', 'created_at', 'updated_at')
    
    # Enable editing users directly in the admin
    filter_horizontal = ('users',)

    def display_users(self, obj):
        # Join user names into a comma-separated string
        return ", ".join([str(user) for user in obj.users.all()])
    
    # Optional: Give a more human-readable name for the custom column
    display_users.short_description = 'Users'

admin.site.register(CreatePanel, CreatePanelAdmin)

admin.site.unregister(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = (
        'question',
        'points',
        'duration',
        'title',
        'mode_of_payment',
        'mode_of_interview',
        'incentive',
        'start_date',
        'end_date',
        'is_active',
        'created_at',
    )
    # Fields to add search functionality
    search_fields = ('question', 'title', 'mode_of_payment', 'mode_of_interview', 'incentive')
    # Fields to filter by
    list_filter = ('is_active', 'start_date', 'end_date')
    # Fields to display in the detail view
    readonly_fields = ('created_at',)
    # Enable the selection of many-to-many fields
    filter_horizontal = ('panels',)

    def question_type(self, obj):
        return dict(SurveyQuestion.QUESTION_TYPES).get(obj.question_type)

# Register the model with the admin site
admin.site.register(SurveyQuestion, SurveyQuestionAdmin)


