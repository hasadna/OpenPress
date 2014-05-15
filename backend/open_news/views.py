# Create your views here.
from django.http import HttpResponse
from django import forms

def search(query):
    pass

def get_search(request):
    
    if 'query' in request.GET:
        search(request.GET['query'])

    return HttpResponse("search has been send")
