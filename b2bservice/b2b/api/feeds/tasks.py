
from celery import shared_task
from api.feeds.utils import fetch_feeds,extract_unique_tags

@shared_task
def update_feeds():
    fetch_feeds()
    extract_unique_tags()




