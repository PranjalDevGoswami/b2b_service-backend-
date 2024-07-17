from django.db import models
from api.account.models import UserModel
from django.contrib.auth import get_user_model
from django.conf import settings
from api.account.models import *

User = get_user_model()


class Language(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
    
class SurveyQuestion(models.Model):
    TEXT = 'text'
    SINGLE_SELECT = 'single_select'
    MULTI_SELECT = 'multi_select'

    QUESTION_TYPES = [
        (TEXT, 'Text'),
        (SINGLE_SELECT, 'Single Select'),
        (MULTI_SELECT, 'Multi Select'),
    ]

    question = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default=TEXT)
    options = models.JSONField(blank=True, null=True, help_text="JSON array of options for single or multi select questions")
    points = models.IntegerField(default=0)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_%(class)s', on_delete=models.CASCADE, blank=True, null=True)
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    time_zone = models.CharField(max_length=255, null=True, blank=True)
    no_of_questions = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.question    


class SurveyAnswer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True, null=True)  # For 'text' type questions
    answer_single_select = models.CharField(max_length=255, blank=True, null=True)  # For 'single_select' type questions
    answer_multi_select = models.JSONField(blank=True, null=True)  # For 'multi_select' type questions
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.question.question}'


class Interview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    date = models.DateTimeField()
    duration = models.DurationField()
    completed = models.BooleanField(default=False)
    voucher = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

class MissedInterview(models.Model):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE)
    missed_at = models.DateTimeField(auto_now_add=True)

class Reward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField()
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.points} points"
    
    

class Community(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CommunityMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'community')


class CommunityPost(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} in {self.community.name}"

class CommunityComment(models.Model):
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.post.content}"

class CommunityLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')    