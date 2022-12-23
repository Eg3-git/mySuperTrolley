from django.urls import path
from trolley import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('searchresults/', views.searchResults, name='searchResults'),
    path('account/', views.account, name='account'),
    path('checkout/', views.checkout, name='checkout'),
    path('product/(<slug:pname_slug>/', views.productPage, name='product'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('basket/', views.basket, name='basket'),
    path('place-order/', views.placeOrder, name='place-order'),
    path('my-orders/', views.my_orders, name='my-orders'),

]
