from django.contrib import admin

from .models import FeedEntry,Tag, UserTagSelection
# Register your models here.

admin.site.register(FeedEntry)
admin.site.register(Tag)
admin.site.register(UserTagSelection)