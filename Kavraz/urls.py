from django.urls import path
from . import views
from products.views import products_detail

urlpatterns = [
    path('', views.home),
    path('home/', views.home),
    path('<slug:slug>//', products_detail, name='products_detail'),
    path('about/', views.about),
]
