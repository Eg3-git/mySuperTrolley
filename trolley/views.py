from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context_dict = {'title': "Homepage"}
    return render(request, 'trolley/index.html', context=context_dict)

def searchResults(request):
    context_dict = {'title': "Search Results"}
    return render(request, 'trolley/searchresults.html', context=context_dict)

def account(request):
    context_dict = {'title': "Account"}
    return render(request, 'trolley/account.html', context=context_dict)

def checkout(request):
    context_dict = {'title': "Checkout"}
    return render(request, 'trolley/checkout.html', context=context_dict)

def productPage(request):
    context_dict = {'title': "Product"}
    return render(request, 'trolley/product.html', context=context_dict)

# Create your views here.
