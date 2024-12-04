from django.shortcuts import render,redirect,get_object_or_404
from .models import Cart, Cart_item
from django.core.exceptions import ObjectDoesNotExist
from store.models import product
from myapp.models import *
from django.contrib import messages

# Create your views here.

def _cart_id(request):
    cart=request.session.session_key
    print(cart)
    if not cart:
        cart=request.session.create()
    return cart

def cart(request,total=0,quantity=0,cart_items=None):
    tax=0
    grand_total=0
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=Cart_item.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total=cart_item.Product.price * cart_item.quantity
            quantity+=cart_item.quantity
            tax=(2*total)/100
            grand_total=total+tax
    except ObjectDoesNotExist:
        pass
    context={'total':total,'quantity':quantity,'cart_items':cart_items,'tax':tax,'grand_total':grand_total}
    return render(request,'cart.html',context)


def add_cart(request, product_id):
    Product = get_object_or_404(product, id=product_id)
    cart_id = _cart_id(request)
    
    if request.user.is_authenticated:
        current_user = customerprofile.objects.filter(user__id=request.user.id)
        cart_str = str(cart_id).replace("'", "\"")
        current_user.update(old_cart=str(cart_str))
        user = request.user
    else:
        user = None
    
    if not cart_id:
        messages.error(request, 'An error occurred. Please try again.')
        return redirect('shop')  # or another fallback page

    cart, created = Cart.objects.get_or_create(cart_id=cart_id, defaults={'user': user})
    
    cart_item, created = Cart_item.objects.get_or_create(cart=cart, Product=Product, user=user)

    if created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1

    # Check stock before saving
    if Product.stock >= cart_item.quantity:
        Product.stock -= 1
        Product.save()
        cart_item.save()
    else:
        messages.info(request, 'Out of stock')

    return redirect('cart')
        
def clear_cart(request):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    cart_item=Cart_item.objects.filter(cart=cart)
    cart_item.delete()
    return redirect('cart')

def remove_from_cart(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    Product=get_object_or_404(product, id=product_id)
    
    try:
        cart_item=Cart_item.objects.get(cart=cart,Product=Product)
        Product.save()
        cart_item.delete()
    except Cart_item.DoesNotExist:
        pass
    
    return redirect('cart')

def decrement_item(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    Product = get_object_or_404(product, id=product_id)
    try:
        cart_item=Cart_item.objects.get(cart=cart,Product=Product)
        
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

            Product.stock += 1
            Product.save()
        else:
            cart_item.delete()
            Product.stock += 1
            Product.save()
           
    except Cart_item.DoesNotExist:
        messages.info(request, 'Item does not exist in the cart.')

    return redirect('cart')

def increment_item(request,product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    Product = get_object_or_404(product, id=product_id)
    cart_items = Cart_item.objects.filter(cart=cart, Product=Product)
    
    if cart_items.exists():
        for cart_item in cart_items:
            if Product.stock <= cart_item.quantity:
                a=Product.stock - cart_item.quantity
                print(a)
                
                messages.warning(request, f"Only {Product.stock - cart_item.quantity} units of this product are available.")
                return redirect('cart')

            cart_item.quantity += 1
            cart_item.save()
        
    return redirect('cart')

