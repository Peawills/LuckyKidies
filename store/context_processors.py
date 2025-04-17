from .cart import get_cart_items_count
from .models import Category

def cart_items_count(request):
    return {
        'cart_items_count': get_cart_items_count(request)
    }



def category_context(request):
    new_categories = Category.objects.filter(category_type="new")
    thrift_categories = Category.objects.filter(category_type="thrift")
    return {
        'new_categories': new_categories,
        'thrift_categories': thrift_categories
    }
