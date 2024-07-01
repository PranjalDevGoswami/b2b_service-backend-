from django.core.management.base import BaseCommand
from feeds.utils import fetch_feeds

class Command(BaseCommand):
    help = 'Fetches and updates feed entries from external sources'

    def handle(self, *args, **kwargs):
        fetch_feeds()
        self.stdout.write(self.style.SUCCESS('Successfully updated feed entries'))
