from .models import Cart, CartItem, Product

def get_cart(request):
    """
    Get or create a cart for the current user or session
    """
    cart_id = request.session.get('cart_id')
    
    if cart_id:
        try:
            cart = Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            cart = create_cart(request)
    else:
        cart = create_cart(request)
    
    return cart

def create_cart(request):
    """
    Create a new cart for the current user or session
    """
    cart = Cart.objects.create(
        user=request.user if request.user.is_authenticated else None,
        session_id=request.session.session_key
    )
    request.session['cart_id'] = cart.id
    return cart

def add_to_cart(request, product_id, quantity=1):
    """
    Add a product to the cart
    """
    cart = get_cart(request)
    product = Product.objects.get(id=product_id)
    
    # Check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    # If the product is already in the cart, update the quantity
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    return cart_item

def remove_from_cart(request, cart_item_id):
    """
    Remove a product from the cart
    """
    cart = get_cart(request)
    try:
        cart_item = CartItem.objects.get(id=cart_item_id, cart=cart)
        cart_item.delete()
        return True
    except CartItem.DoesNotExist:
        return False

def update_cart_item_quantity(request, cart_item_id, quantity):
    """
    Update the quantity of a cart item
    """
    cart = get_cart(request)
    try:
        cart_item = CartItem.objects.get(id=cart_item_id, cart=cart)
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        return True
    except CartItem.DoesNotExist:
        return False

def get_cart_items_count(request):
    """
    Returns the total quantity of all items in the user's cart.
    """
    cart = get_cart(request)
    items = cart.items.all()
    total_quantity = sum(item.quantity for item in items)
    return total_quantity
