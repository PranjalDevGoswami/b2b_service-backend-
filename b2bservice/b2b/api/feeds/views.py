from django.shortcuts import render
import feedparser
import requests
import xml.etree.ElementTree as ET
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
User = get_user_model()

def fetch_feed(url, headers=None, limit=10):
    response = requests.get(url, headers=headers)
    root = ET.fromstring(response.content)

    items = []
    for item in root.findall('.//item')[:limit]:
        title = item.find('title').text
        description = item.find('description').text
        link = item.find('link').text
        items.append({'title': title, 'description': description, 'link': link})

    return items


from django.http import JsonResponse
from django.views import View

class FeedView(View):
    def get(self, request):
        feeds = {
            'finance': 'https://api.bloomberg.com/syndication/rss/v1/news/13aa5e44-c5e3-4ca8-a907-494a390f43cd?access_token=c1ff41a9415aa8bfcf0209217fca37c0',
            'economics': 'https://economictimes.indiatimes.com/rssfeedsdefault.cms',
            # Add more feed URLs here
        }

        headers = {
            'Authorization': 'Bearer your_bloomberg_api_key'
        }

        data = {}
        for key, url in feeds.items():
            if key == 'finance':
                data[key] = fetch_feed(url, headers=headers, limit=10)
            else:
                data[key] = fetch_feed(url)

        return JsonResponse(data)



from rest_framework import generics
from .models import FeedEntry
from .serializers import FeedEntrySerializer
from rest_framework import filters



class FeedList(generics.ListAPIView):
    queryset = FeedEntry.objects.all()
    serializer_class = FeedEntrySerializer
    # filter_backends = [DjangoFilterBackend]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['source', 'tags']

    def get_queryset(self):
        queryset = FeedEntry.objects.all()
        source = self.request.query_params.get('source', None)
        tags = self.request.query_params.getlist('tags', None)
        
        if source:
            queryset = queryset.filter(source=source)
        
        if tags:
            queryset = queryset.filter(tags__name__in=tags).distinct()
        
        return queryset
    
    


class TagListView(generics.ListAPIView):
    """
    List tags based on the user's industry and category.
    """
    serializer_class = TagSerializer

    def get_queryset(self):
        # Assuming the user has an industry and category profile, you can filter based on that
        user = self.request.user
        industry_id = self.request.query_params.get('industry')
        category_id = self.request.query_params.get('category')
        
        if industry_id and category_id:
            return Tag.objects.filter(category__industry_id=industry_id, category_id=category_id)
        return Tag.objects.none()

class UserTagSelectionView(generics.CreateAPIView):
    """
    Allow users to select tags (like skills/interests).
    """
    serializer_class = UserTagSelectionSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        tag_ids = request.data.get('tag_ids', [])
        
        for tag_id in tag_ids:
            tag = Tag.objects.get(id=tag_id)
            UserTagSelection.objects.get_or_create(user=user, tag=tag)
        
        return Response({'message': 'Tags saved successfully'}, status=status.HTTP_201_CREATED)  