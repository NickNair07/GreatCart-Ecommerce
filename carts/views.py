from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, Cart_item
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Variation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)    # get the product with product id

    # if user is authenticated
    if current_user.is_authenticated:

        # get product variaion - color and size
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass


        # for getting the cart item
            # to check the cart item is present in the cart
        is_cart_item_exists = Cart_item.objects.filter(product=product, user=current_user).exists()

        if is_cart_item_exists:
            cart_item = Cart_item.objects.filter(product=product, user=current_user)
            # to check the variation is present in the cart item
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # increase the same cart item
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = Cart_item.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                # create a new cart item with different variation
                item = Cart_item.objects.create(product=product, quantity=1, user=current_user)
                # to check the product variaton list is empty or not:
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()

        # adding the cart item first time with a session key and setting the quantity = 1
        else:         
            cart_item = Cart_item.objects.create(product=product,quantity=1,user=current_user,)
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')

    # if the user is not authenticated
    else:
        # get product variaion - color and size
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        # for getting the cart 
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))   # get the cart using session key 

        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id = _cart_id(request))   # if cart not exist, create cart using session key
            cart.save()

        # for getting the cart item
        # to check the cart item is present in the cart
        is_cart_item_exists = Cart_item.objects.filter(product=product, cart=cart).exists()

        if is_cart_item_exists:
            cart_item = Cart_item.objects.filter(product=product, cart=cart)
            # to check the variation is present in the cart item
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # increase the same cart item
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = Cart_item.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                # create a new cart item with different variation
                item = Cart_item.objects.create(product=product, quantity=1, cart=cart)
                # to check the product variaton list is empty or not:
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()

        # adding the cart item first time with a session key and setting the quantity = 1
        else:         
            cart_item = Cart_item.objects.create(product=product,quantity=1,cart=cart,)
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')


# function for decrement the cart item
def remove_cart(request, product_id, cart_item_id):
    
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = Cart_item.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id= _cart_id(request))
            cart_item = Cart_item.objects.get(product=product, cart=cart, id=cart_item_id)
    
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


# function for remove the cart item
def remove_cart_item(request, product_id, cart_item_id):
    
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = Cart_item.objects.get(cart=cart, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))      # get the cart using session key
        cart_item = Cart_item.objects.get(cart=cart, product=product, id=cart_item_id)   # get the cart item related to the specific cart
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = Cart_item.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id= _cart_id(request)) 
            cart_items = Cart_item.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass


    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = Cart_item.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id= _cart_id(request)) 
            cart_items = Cart_item.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
        
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)