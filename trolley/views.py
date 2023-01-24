import json
import random
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from trolley.models import Product
from django.db.models import Q
from trolley.forms import *
from django.contrib.auth import authenticate, login, logout, decorators
from django.urls import reverse


def get_basket(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        details = {'user_logged_in': True, 'has_items': False, 'basket_items': items, 'order': order}
        if len(items) > 0:
            details['has_items'] = True
        return details
    else:
        return {'user_logged_in': False}


def generate_context_dict(request, other_context=None):
    context = {'basket_details': get_basket(request)}
    if other_context is not None:
        context.update(other_context)
    return context


def index(request, ordered=False):
    product_count = Product.objects.count()
    suggested_ids = random.sample(range(1, product_count + 1), 10)
    suggestions = [Product.objects.get(id=p) for p in suggested_ids]

    context_dict = generate_context_dict(request, {'ordered': ordered, 'suggestions': suggestions})

    return render(request, 'trolley/index.html', context=context_dict)


def about(request):
    return render(request, 'trolley/about.html')


def searchResults(request, query=None):
    context_dict = generate_context_dict(request)

    if query is None:
        query = request.GET.get("q")

    results = Product.objects.filter(Q(name__icontains=query))
    context_dict['products'] = results
    context_dict['search_term'] = query
    return render(request, 'trolley/searchresults.html', context=context_dict)


def readyResults(request, query):
    return searchResults(request, query)


def basket(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        retailers = {}
        for orderItem in items:
            if orderItem.product.retailer in retailers:
                retailers[orderItem.product.retailer].append(orderItem)
            else:
                retailers[orderItem.product.retailer] = [orderItem]
        context = {'items': items, 'order': order, 'retailers': retailers}
        return render(request, 'trolley/basket.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))




def account(request):
    context_dict = generate_context_dict(request)
    return render(request, 'trolley/account.html', context=context_dict)


def my_orders(request):
    customer = request.user
    orders = Order.objects.filter(customer=customer, complete=True)
    orderinfo = []
    for order in orders:
        orderinfo.append((order, order.orderitem_set.all()))
    context = generate_context_dict(request, {'orders': orderinfo})

    if len(orderinfo) == 0:
        context['has_orders'] = False
    else:
        context['has_orders'] = True

    return render(request, 'trolley/orders.html', context=context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        totalQuantity = order.get_basket_quantities
    else:
        items = []
        order = {'calculate_basket_total': 0, 'get_basket_quantities': 0, 'shipping': False}
        totalQuantity = order['get_basket_quantities']
    context_dict = {'items': items, 'order': order, 'totalQuantity': totalQuantity}
    return render(request, 'trolley/checkout.html', context=context_dict)


def productPage(request, pname_slug):
    product = Product.objects.get(slug=pname_slug)
    context_dict = generate_context_dict(request, {'in_basket': False, 'product': product})

    if request.user.is_authenticated:
        customer = request.user
        order = Order.objects.get_or_create(customer=customer, complete=False)[0]
        basket_items = order.orderitem_set.all()
        for item in basket_items:
            if item.product.id == product.id:
                context_dict['in_basket'] = True
                break

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
            return render(request, 'trolley/login.html', {'attempted_login': True})

    else:
        return render(request, 'trolley/login.html', {'attempted_login': False})


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
