from django.shortcuts import render
from django.http import HttpResponse


def ApiStatus(request):
    return HttpResponse("Status code 200")