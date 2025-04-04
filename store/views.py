from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Product, Category
from .cart import get_cart, add_to_cart, remove_from_cart, update_cart_item_quantity, get_cart_items_count
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def clear_session(request):
    if request.method == 'POST':
        request.session.flush()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'store/search_results.html', {'products': products, 'query': query})

def home(request):
    products = Product.objects.all().filter(is_available=True)
    new_categories = Category.objects.filter(category_type="new")
    thrift_categories = Category.objects.filter(category_type="thrift")
    context = {
        'products': products,
        'new_categories': new_categories,
        'thrift_categories': thrift_categories,
    }
    return render(request, 'home.html', context)

def new_clothing(request):
    products = Product.objects.filter(condition='new', is_available=True)
    context = {
        'products': products,
        'title': 'New Clothing'
    }
    return render(request, 'store/product_list.html', context)

def thrift_clothing(request):
    products = Product.objects.filter(condition='thrift', is_available=True)
    context = {
        'products': products,
        'title': 'Thrift Clothing'
    }
    return render(request, 'store/product_list.html', context)

def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    context = {
        'product': product,
    }
    return render(request, 'store/product_detail.html', context)

def products_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, is_available=True)
    context = {
        'products': products,
        'category': category,
    }
    return render(request, 'store/product_list.html', context)

def cart_detail(request):
    cart = get_cart(request)
    context = {
        'cart': cart,
        'whatsapp_number': settings.WHATSAPP_NUMBER,
    }
    return render(request, 'store/cart.html', context)

def add_to_cart_view(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        try:
            cart_item = add_to_cart(request, product_id, quantity)
            messages.success(request, f"{cart_item.product.name} added to your cart.")
            return JsonResponse({
                'success': True,
                'message': f"{cart_item.product.name} added to your cart.",
                'cart_count': get_cart_items_count(request)
            })
        except Product.DoesNotExist:
            messages.error(request, "Product not found.")
            return JsonResponse({
                'success': False,
                'message': "Product not found."
            })
    return JsonResponse({
        'success': False,
        'message': "Invalid request method."
    })

def remove_from_cart_view(request, cart_item_id):
    if request.method == 'POST':
        success = remove_from_cart(request, cart_item_id)
        if success:
            messages.success(request, "Item removed from your cart.")
            return JsonResponse({
                'success': True,
                'message': "Item removed from your cart.",
                'cart_count': get_cart_items_count(request)
            })
        else:
            messages.error(request, "Item not found in your cart.")
            return JsonResponse({
                'success': False,
                'message': "Item not found in your cart."
            })
    return JsonResponse({
        'success': False,
        'message': "Invalid request method."
    })

def update_cart_item_view(request, cart_item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 0))
        success = update_cart_item_quantity(request, cart_item_id, quantity)
        if success:
            messages.success(request, "Cart updated successfully.")
            return JsonResponse({
                'success': True,
                'message': "Cart updated successfully.",
                'cart_count': get_cart_items_count(request)
            })
        else:
            messages.error(request, "Item not found in your cart.")
            return JsonResponse({
                'success': False,
                'message': "Item not found in your cart."
            })
    return JsonResponse({
        'success': False,
        'message': "Invalid request method."
    })
def products_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, is_available=True)
    context = {
        'products': products,
        'category': category,
    }
    return render(request, 'store/product_list.html', context)