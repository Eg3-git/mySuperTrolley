from django.urls import path
from trolley import views

urlpatterns = [
    path('', views.index, name='index'),
    path('searchresults/', views.searchResults, name='searchResults')
]
