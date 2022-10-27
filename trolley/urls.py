from django.urls import path
from trolley import views

urlpatterns = [
    path('', views.index, name='index'),
    path('searchresults/', views.searchResults, name='searchResults'),
    path('account/', views.account, name='account'),
    path('checkout/', views.checkout, name='checkout'),
    path('product/', views.productPage, name='product'),
]
