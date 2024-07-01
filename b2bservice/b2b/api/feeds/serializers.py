from rest_framework import serializers
from .models import FeedEntry

class FeedEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedEntry
        fields = ['source', 'title', 'link', 'summary', 'published']
