from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, Cart_item
from store.models import Product

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)    # get the product with product id
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))   # get the cart using session key 

    except Cart.DoesNotExist:
        cart = Cart.objects.create(                 # if cart not exist, create cart using session key
            cart_id = _cart_id(request)
        )
        cart.save()

    try:
        cart_item = Cart_item.objects.get(product=product, cart=cart)    # get cart item to the cart
        cart_item.quantity += 1          # increase the cart item quantity
        cart_item.save()
    except Cart_item.DoesNotExist:          # adding the cart item first time with a session key-
                                                                            # and setting the quantity = 1
        cart_item = Cart_item.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        cart_item.save()
    return redirect('cart')


def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id= _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = Cart_item.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))      # get the cart using session key
    product = get_object_or_404(Product, id=product_id)     
    cart_item = Cart_item.objects.get(cart=cart, product=product)   # get the cart item related to the specific cart
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    cart = Cart.objects.get(cart_id= _cart_id(request)) 
    cart_items = Cart_item.objects.filter(cart=cart, is_active=True)

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    tax = (2 * total)/100
    grand_total = total + tax

    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, 'store/cart.html', context)