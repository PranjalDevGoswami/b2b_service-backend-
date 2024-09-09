from django.db import models
from api.account.models import Trackable
from api.account.models import Category
from django.contrib.auth import get_user_model
user = get_user_model()
# Create your models here.
from django.db import models

class Tag(Trackable):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tags', null=True, blank=True)
     
    def __str__(self):
        return self.name


class FeedEntry(Trackable):
    source = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    image_link = models.URLField(blank=True, null=True)  
    summary = models.TextField(null=True, blank=True)
    published = models.DateTimeField(null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    

    class Meta:
        unique_together = ('source', 'link') 

    def __str__(self):
        return self.title



class UserTagSelection(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name='selected_tags', null=True, blank=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.tag.name}'