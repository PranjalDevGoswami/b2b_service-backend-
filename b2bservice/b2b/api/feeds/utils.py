import feedparser
from datetime import datetime
from .models import FeedEntry
import logging

logger = logging.getLogger(__name__)

import feedparser
from datetime import datetime
from .models import FeedEntry, Tag

FEEDS = {
    'wsj_us_business': 'https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml',
    'wsj_markets': 'https://feeds.a.dj.com/rss/RSSMarketsMain.xml',
    'economic_times': 'https://economictimes.indiatimes.com/rss.cms',
    'bloomberg': 'https://api.bloomberg.com/syndication/rss/v1/news/13aa5e44-c5e3-4ca8-a907-494a390f43cd?access_token=c1ff41a9415aa8bfcf0209217fca37c0'
    
}

# def fetch_feeds():
#     feeds = []
#     for source, url in FEEDS.items():
#         feed = feedparser.parse(url)
#         for entry in feed.entries:
#             link = entry.get('link', None)
#             if link:
#                 published = datetime(*entry.published_parsed[:6])
#                 feed_entry, created = FeedEntry.objects.get_or_create(
#                     source=source,
#                     link=link,
#                     defaults={
#                         'title': entry.title,
#                         'summary': entry.summary,
#                         'published': published
#                     }
#                 )
#                 if created:
#                     # Assuming tags are available in some form in the entry
#                     tags_data = entry.get('tags', [])
#                     tags = [Tag.objects.get_or_create(name=tag)[0] for tag in tags_data]
#                     feed_entry.tags.add(*tags)
#                     feed_entry.save()
#                     feeds.append(feed_entry)
#             else:
#                 logger.warning(f"Entry missing 'link' attribute in feed '{source}': {entry}")
#     return feeds

# def fetch_feeds():
#     feeds = []
#     for source, url in FEEDS.items():
#         feed = feedparser.parse(url)
#         for entry in feed.entries:
#             link = entry.get('link', None)
#             image_link = None
#             # Try to extract image link from media content or enclosure
#             if 'media_content' in entry:
#                 image_link = entry.media_content[0]['url']  # Common in many feeds
#             elif 'enclosure' in entry:
#                 image_link = entry.enclosure.get('url')
            
#             if link:
#                 published = datetime(*entry.published_parsed[:6])
#                 feed_entry, created = FeedEntry.objects.get_or_create(
#                     source=source,
#                     link=link,
#                     defaults={
#                         'title': entry.title,
#                         'summary': entry.summary,
#                         'published': published,
#                         'image_link': image_link  # Save the image link
#                     }
#                 )
#                 if created:
#                     tags_data = entry.get('tags', [])
#                     tags = [Tag.objects.get_or_create(name=tag)[0] for tag in tags_data]
#                     feed_entry.tags.add(*tags)
#                     feed_entry.save()
#                     feeds.append(feed_entry)
#             else:
#                 logger.warning(f"Entry missing 'link' attribute in feed '{source}': {entry}")
#     return feeds

import feedparser
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def fetch_feeds():
    feeds = []
    for source, url in FEEDS.items():
        feed = feedparser.parse(url)
        # print("feed", feed)
        for entry in feed.entries:
            link = entry.get('link', None)
            image_link = None

            # Try to extract image link from media content, enclosure, or other potential fields
            if 'media_content' in entry:
                # Check if media_content contains image URLs
                for media in entry.media_content:
                    if 'medium' in media and media['medium'] == 'image':
                        image_link = media.get('url')
                        break  # Stop at the first image found

            elif 'media_thumbnail' in entry:
                # Some feeds use media_thumbnail for image links
                image_link = entry.media_thumbnail[0].get('url')

            elif 'enclosure' in entry:
                # Enclosure might also contain image links
                if 'type' in entry.enclosure and 'image' in entry.enclosure['type']:
                    image_link = entry.enclosure.get('url')

            if link:
                published = datetime(*entry.published_parsed[:6])
                feed_entry, created = FeedEntry.objects.get_or_create(
                    source=source,
                    link=link,
                    defaults={
                        'title': entry.title,
                        'summary': entry.summary,
                        'published': published,
                        'image_link': image_link  # Save the image link
                    }
                )
                if created:
                    tags_data = entry.get('tags', [])
                    tags = [Tag.objects.get_or_create(name=tag)[0] for tag in tags_data]
                    feed_entry.tags.add(*tags)
                    feed_entry.save()
                    feeds.append(feed_entry)
            else:
                logger.warning(f"Entry missing 'link' attribute in feed '{source}': {entry}")
    return feeds
