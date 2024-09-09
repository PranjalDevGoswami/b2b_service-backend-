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
        
# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = ['id', 'name']

class TagSerializer(serializers.ModelSerializer):
    # Add the category field, which can be None if no category is associated
    category = CategorySerializer(allow_null=True, required=False)
    
    # Add a feed list for each tag
    feeds = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ['id', 'name', 'category', 'feeds']  # Include feeds in the response

    # Method to retrieve feeds related to the tag
    def get_feeds(self, obj):
        # Filter FeedEntry by the tag
        feeds = FeedEntry.objects.filter(tags=obj)
        print('object',obj)
        print('feeds', feeds)
        return FeedEntrySerializer(feeds, many=True).data


        

class FeedEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedEntry
        fields = ['source', 'title', 'link','image_link', 'summary', 'published','tags']


class UserTagSelectionSerializer(serializers.ModelSerializer):
    tag = TagSerializer()

    class Meta:
        model = UserTagSelection
        fields = ['id', 'tag', 'created_at']