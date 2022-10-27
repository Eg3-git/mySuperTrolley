from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context_dict = {'title': "Homepage"}
    return render(request, 'trolley/index.html', context=context_dict)

def searchResults(request):
    return render(request, 'trolley/searchresults.html')

def account(request):
    return render(request, 'trolley/account.html')

def checkout(request):
    return render(request, 'trolley/checkout.html')

def productPage(request):
    return render(request, 'trolley/product.html')

# Create your views here.
