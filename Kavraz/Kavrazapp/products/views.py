from django.shortcuts import render, get_object_or_404
from .models import products, category 
from django.db.models import Q
import string

def products_view(request,):
    products_list = products.objects.filter(isActive=True)
    categories = category.objects.filter(isActive=True)

    category_filter = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    selected_category_obj = None
    if category_filter:
        products_list = products_list.filter(category__slug=category_filter)
        selected_category_obj = get_object_or_404(category, slug=category_filter)
    
    if min_price:
        products_list = products_list.filter(price__gte=min_price)
    
    if max_price:
        products_list = products_list.filter(price__lte=max_price)
    
    return render(request, 'products/products.html', {
        "products": products_list,
        "categories": categories,
        "selected_category": category_filter,
        "selected_category_obj": selected_category_obj,
        "min_price": min_price,
        "max_price": max_price,
    })

def products_detail(request, slug):
    product = get_object_or_404(products, slug=slug)
    related_products = products.objects.filter(
        category=product.category,
        isActive=True
    ).exclude(id=product.id)[:4]  # Aynı kategoriden 4 ürün getir
    
    return render(request, 'products/products-detail.html', {
        'no_item': product,
        'products': related_products 
    })

def search_results(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = products.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            isActive=True
        )

    categories = category.objects.filter(isActive=True)

    # Filtreleme
    category_filter = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    selected_category_obj = None
    if category_filter:
        results = results.filter(category__slug=category_filter)
        selected_category_obj = get_object_or_404(category, slug=category_filter)

    if min_price:
        results = results.filter(price__gte=min_price)

    if max_price:
        results = results.filter(price__lte=max_price)

    big_query = string.capwords(query)

    return render(request, 'products/search_results.html', {
        'query': big_query,
        'products': results,
        "categories": categories,
        "selected_category": category_filter,
        "selected_category_obj": selected_category_obj,
        "min_price": min_price,
        "max_price": max_price,
    })