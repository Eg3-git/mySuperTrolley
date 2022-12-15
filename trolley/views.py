import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from trolley.models import Product
from django.db.models import Q
from trolley.forms import *
from django.contrib.auth import authenticate, login, logout, decorators
from django.urls import reverse


def index(request, ordered=False):
    context_dict = {'title': "Homepage", 'ordered': ordered, 'products': Product.objects.all()[1:6]}

    return render(request, 'trolley/index.html', context=context_dict)


def searchResults(request):
    context_dict = {'title': "Search Results"}
    query = request.GET.get("q")
    results = Product.objects.filter(Q(name__icontains=query))
    context_dict['products'] = results
    return render(request, 'trolley/searchresults.html', context=context_dict)

def basket(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'calculate_basket_total':0, 'get_basket_quantities':0}

    context = {'items':items, 'order':order}
    return render(request, 'trolley/basket.html', context)


def account(request):
    context_dict = {'title': "Account"}
    return render(request, 'trolley/account.html', context=context_dict)

def my_orders(request):
    customer = request.user
    orders = Order.objects.filter(customer=customer, complete=True)
    orderinfo = []
    for order in orders:
        orderinfo.append((order, order.orderitem_set.all()))
    context = {'orders':orderinfo}
    return render(request, 'trolley/orders.html', context=context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        totalQuantity = order.get_basket_quantities
    else:
        items = []
        order = {'calculate_basket_total':0, 'get_basket_quantities':0, 'shipping':False}
        totalQuantity = order['get_basket_quantities']
    context_dict = {'items': items, 'order':order, 'totalQuantity':totalQuantity}
    return render(request, 'trolley/checkout.html', context=context_dict)


def productPage(request, pname_slug):
    context_dict = {'title': "Product"}

    try:
        products = Product.objects.get(slug=pname_slug)
        context_dict['product'] = products
    except Product.DoesNotExist:
        context_dict['product'] = None

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

def updateItem(request):
    data = json.loads(request.body)
    pID = data['productID']
    action = data['action']

    customer = request.user
    product = Product.objects.get(id=pID)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item added", safe=False)

def placeOrder(request):

    if request.method == 'POST':
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order.complete = True
        ordered = True
        order.save()
    else:
        ordered = False

    return index(request, ordered)
