from django.shortcuts import render

# Create your views here.
import feedparser
import requests

import requests
import xml.etree.ElementTree as ET

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
    
# from django.http import JsonResponse
# from django.views import View

# class FeedView(View):
#     def get(self, request):
#         # feeds = {
#         #     'bloomberg': 'https://api.bloomberg.com/syndication/rss/v1/news/13aa5e44-c5e3-4ca8-a907-494a390f43cd?access_token=c1ff41a9415aa8bfcf0209217fca37c0',
#         #     'economic_times': 'https://economictimes.indiatimes.com/rssfeedsdefault.cms',
#         #     # Add more feed URLs here
#         # }
        
#         feeds = {
#             'finance': 'https://api.bloomberg.com/syndication/rss/v1/news/13aa5e44-c5e3-4ca8-a907-494a390f43cd?access_token=c1ff41a9415aa8bfcf0209217fca37c0',
#             'economics': 'https://economictimes.indiatimes.com/rssfeedsdefault.cms',
#             # Add more feed URLs here
        
#         }
#         headers = {
#             'Authorization': 'Bearer your_bloomberg_api_key'
#         }

#         data = {}
#         for key, url in feeds.items():
#             if key == 'economics':
#                 data[key] = fetch_feed(url, headers=headers)
#             else:
#                 data[key] = fetch_feed(url)

#         return JsonResponse(data)

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

class FeedList(generics.ListAPIView):
    queryset = FeedEntry.objects.all()
    serializer_class = FeedEntrySerializer

    def get_queryset(self):
        queryset = FeedEntry.objects.all()
        source = self.request.query_params.get('source', None)
        if source is not None:
            queryset = queryset.filter(source=source)
        return queryset

    