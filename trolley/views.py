from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context_dict = {'title': "Homepage"}
    return render(request, 'trolley/index.html', context=context_dict)

def searchResults(request):
    return render(request, 'trolley/searchresults.html')

# Create your views here.
