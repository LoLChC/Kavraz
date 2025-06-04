from django.urls import path
from . import views

urlpatterns = [
    path('', views.products_view, name='products'),
    path('search/', views.search_results, name='search_results'),  # Önce özel yollar gelmeli
    path('<slug:slug>/', views.products_detail, name='products_detail'),
]
