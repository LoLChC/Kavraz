from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.products_view, name='products'),
    path('search/', views.search_results, name='search_results'),
    path('sepet/', views.view_cart, name='view_cart'),
    path('sepet/ekle/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('sepet/sil/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('sepet/guncelle/<int:item_id>/', views.update_cart, name='update_cart'),
    path('odeme/', views.checkout, name='checkout'),
    path('<slug:slug>/', views.products_detail, name='products_detail'),
]