from django.contrib import admin

from .models import FeedEntry,Tag
# Register your models here.

admin.site.register(FeedEntry)
admin.site.register(Tag)