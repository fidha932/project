from django.shortcuts import get_object_or_404, render
from .models import *
# Create your views here.

def shop(request, category_slug=None):
    context={}
    categories=0
    products=0
    product_count=0
    if category_slug is not None:
        categories=get_object_or_404(category,slug=category_slug)
        products=product.objects.filter(Category=categories,is_available=True)
        product_count=products.count()
    else:
        products=product.objects.filter(is_available=True)
        product_count=products.count()
        
    context={
        'products':products, 
        'categories':categories,
        'product_count':product_count
    }
    return render(request,'product_page.html',context)




def product_detail(request ,category_slug ,product_slug):
    try:
        single_product=product.objects.get(category__slug=category_slug,slug=product_slug)
    except Exception as e:
        raise e 
    context={'single_product':single_product}
    return render(request,'detail.html',context)