from django.shortcuts import render, get_object_or_404, redirect
from .models import products, category, Cart, CartItem
from django.db.models import Q
import string
from django.contrib.auth.decorators import login_required
import random

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
        "random_number": random.randint(1, 1000),
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
        "random_number": random.randint(1, 1000),
        'no_item': product,
        'products': related_products 
    })

def search_results(request):
    query = request.GET.get('q')

    results = products.objects.filter(isActive=True)  # Her durumda bir QuerySet

    if query:
        results = results.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    categories = category.objects.filter(isActive=True)

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

    big_query = string.capwords(query) if query else ""

    return render(request, 'products/search_results.html', {
        "random_number": random.randint(1, 1000),
        'query': big_query,
        'products': results,
        "categories": categories,
        "selected_category": category_filter,
        "selected_category_obj": selected_category_obj,
        "min_price": min_price,
        "max_price": max_price,
    })


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(products, id=product_id)
    
    # Kullanıcının sepetini al veya oluştur
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Formdan miktarı al
    quantity = int(request.POST.get('quantity', 1))
    
    # Stok kontrolü
    if quantity > product.stock:
        return redirect(request.META.get('HTTP_REFERER', 'products:products'))
    
    # Ürün sepette var mı kontrol et
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        # Eğer sepette varsa ve yeni miktar stokları aşmıyorsa güncelle
        new_quantity = cart_item.quantity + quantity
        if new_quantity <= product.stock:
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            pass
    
    return redirect(request.META.get('HTTP_REFERER', 'products:products'))

@login_required
def view_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()  # related_name='items' olduğu için bu şekilde erişiyoruz
        cart_total = sum(item.product.price * item.quantity for item in cart_items)
        
        context = {
            'cart_items': cart_items,
            'cart_total': cart_total,
            "random_number": random.randint(1, 1000),  # Diğer view'larda kullanılan random sayı
        }
        
    except Cart.DoesNotExist:
        # Eğer sepet yoksa boş bir sepet göster
        context = {
            'cart_items': None,
            'cart_total': 0,
            "random_number": random.randint(1, 1000),
        }
    
    return render(request, 'products/cart.html', context)

@login_required
def remove_from_cart(request, item_id):
    if not request.user.is_authenticated:
        return redirect('/account/login')  # Veya giriş sayfanız
    
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('products:view_cart')

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
    
    return redirect('products:view_cart')

@login_required
def checkout(request):
    pass