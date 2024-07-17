from django.contrib import admin

from api.serveyapp.models import *

admin.site.register(SurveyQuestion)
admin.site.register(SurveyAnswer)