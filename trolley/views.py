from django.shortcuts import render
from django.http import HttpResponse
from trolley.models import Product


def index(request):
    context_dict = {'title': "Homepage"}
    context_dict['products'] = Product.objects.all()[1:6]
    for p in context_dict['products']:
        print(p.name, p.slug)
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

def productPage(request, pname_slug):
    context_dict = {'title': "Product"}

    try:
        products = Product.objects.get(slug=pname_slug)
        context_dict['products'] = products
    except Product.DoesNotExist:
        context_dict['products'] = None

    return render(request, 'trolley/product.html', context=context_dict)

# Create your views here.
