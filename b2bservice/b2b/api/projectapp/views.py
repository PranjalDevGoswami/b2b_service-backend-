from django.shortcuts import render, HttpResponse

# Create your views here.

def ApiStatus(request):
    return HttpResponse("Status code 200")