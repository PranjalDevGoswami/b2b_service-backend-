from django.db import models
from api.account.models import Trackable

# Create your models here.
from django.db import models

class FeedEntry(Trackable):
    source = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    published = models.DateTimeField(null=True, blank=True)
    

    class Meta:
        unique_together = ('source', 'link') 

    def __str__(self):
        return self.title
