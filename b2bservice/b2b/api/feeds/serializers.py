from rest_framework import serializers
from .models import *



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class FeedEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedEntry
        fields = ['source', 'title', 'link', 'summary', 'published','tags']
