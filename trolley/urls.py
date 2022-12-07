from django.urls import path
from trolley import views

urlpatterns = [
    path('', views.index, name='index'),
    path('searchresults/', views.searchResults, name='searchResults'),
    path('account/', views.account, name='account'),
    path('checkout/', views.checkout, name='checkout'),
    path('product/(<slug:pname_slug>/', views.productPage, name='product'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('basket/', views.basket, name='basket'),

]
