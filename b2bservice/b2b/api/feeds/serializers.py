from rest_framework import serializers
from .models import *
from api.account.models import *

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    industry = IndustrySerializer()

    class Meta:
        model = Category
        fields = ['id', 'name', 'industry']
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class FeedEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedEntry
        fields = ['source', 'title', 'link','image_link', 'summary', 'published','tags']


class UserTagSelectionSerializer(serializers.ModelSerializer):
    tag = TagSerializer()

    class Meta:
        model = UserTagSelection
        fields = ['id', 'tag', 'created_at']