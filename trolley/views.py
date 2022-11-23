from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from trolley.models import Product
from django.db.models import Q
from trolley.forms import *
from django.contrib.auth import authenticate, login, logout, decorators
from django.urls import reverse


def index(request):
    context_dict = {'title': "Homepage"}
    context_dict['products'] = Product.objects.all()[1:6]

    return render(request, 'trolley/index.html', context=context_dict)


def searchResults(request):
    context_dict = {'title': "Search Results"}
    query = request.GET.get("q")
    results = Product.objects.filter(Q(name__icontains=query))
    context_dict['products'] = results
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


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)

    else:
        user_form = UserForm()

    return render(request, 'trolley/register.html', {'user_form': user_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account disabled")

        else:
            print("Invalid details")
            return HttpResponse("Invalid details")

    else:
        return render(request, 'trolley/login.html', {})


@decorators.login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
