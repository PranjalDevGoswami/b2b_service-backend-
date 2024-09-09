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
from rest_framework_simplejwt.authentication import JWTAuthentication

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
    List tags based on the logged-in user's industry and associated categories.
    Return category if available, otherwise return None for category.
    Also return feeds related to each tag.
    """
    serializer_class = TagSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            user = self.request.user
            
            # Check if the user has an industry associated
            if not user.industry:
                raise NotFound(detail="Industry not found for the user.", code=status.HTTP_404_NOT_FOUND)
            
            industry_id = user.industry.id
           
            # Fetch categories linked to the industry
            categories = Category.objects.filter(industry_id=industry_id).values_list('id', flat=True)

            if not categories.exists():
                raise NotFound(detail="No categories found for the user's industry.", code=status.HTTP_404_NOT_FOUND)

            # Filter tags based on the fetched categories
            queryset = Tag.objects.filter(category_id__in=categories)
            
            if not queryset.exists():
                raise NotFound(detail="No tags found for the selected categories.", code=status.HTTP_404_NOT_FOUND)

            return queryset
        
        except NotFound as e:
            # If a specific NotFound exception is raised, re-raise it
            raise e
        
        except Exception as e:
            # For any other unforeseen exceptions, return a generic error response
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

            
            
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