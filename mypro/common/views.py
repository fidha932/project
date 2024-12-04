from django.shortcuts import render,get_object_or_404,redirect
from store.models import *
from .models import *
from django.utils.text import slugify
from django.core.files.storage import default_storage


# Create your views here.


def addcategory(request):
    if request.method=='POST':
        category_name=request.POST.get('category_name')
        slug=request.POST.get('slug')
        description=request.POST.get('description')
        cat_image=request.FILES.get('cat_image')
        
        if not slug:
            slug = slugify(category_name)
            
        categories= category (
            category_name=category_name,
            slug=slug,
            description=description,
            cat_image=cat_image
        ) 
        categories.save()
    return render(request,'add_category.html')

def allcategory(request):
    a=category.objects.all()
    return render(request,'view_category.html',{'a':a})

def deletecategory(request,category_id):
    categories=get_object_or_404(category, id=category_id)
    categories.delete()
    return redirect('allcategory')

def editcategory(request,category_id):
    m=get_object_or_404(category, id=category_id)
    if request.method=='POST':
        category_name= request.POST.get('category_name')
        slug=request.POST.get('slug')
        description=request.POST.get('description')
        cat_image=request.FILES.get('cat_image')
        m.category_name=category_name
        m.slug=slug
        m.description=description
        if cat_image:
            if m.cat_image:
                default_storage.delete(m.cat_image.name)
            m.cat_image=cat_image
        m.save()
        return redirect('allcategory')
        
    s=category.objects.filter(id=category_id)
    return render(request,'editcategory.html',{'m':s})

def addproduct(request):
    if request.method=='POST':
        product_name=request.POST.get('product_name')
        slug=request.POST.get('slug')
        description=request.POST.get('description')
        price=request.POST.get('price')
        images=request.FILES.get('images')
        stock=request.POST.get('stock')
        is_available=request.POST.get('is_available') == 'on'
        category_id=request.POST.get('category')
        sku=request.POST.get('sku')
        priority=request.POST.get('priority')
        a=category.objects.get(id=category_id)
        if not slug:
            slug=slugify(product_name)
        products=product(
            product_name=product_name,
            slug=slug,
            description=description,
            price=price,
            images=images,
            stock=stock,
            category=a,
            sku=sku,
            priority=priority
        )
        products.save()
    m=category.objects.all()
    return render(request,'add_product.html', {'m':m})

def allproduct(request):
    m=product.objects.all()
    return render(request, 'view_product.html', {'m':m})

def deleteproduct(request, product_id):
    m=get_object_or_404(product, id=product_id)
    m.delete()
    return redirect('allproduct')

def editproduct(request, product_id):
    m= get_object_or_404(product, id=product_id)
    categories = category.objects.all()  

    if request.method == 'POST':
        m.product_name = request.POST.get('product_name')
        m.slug = request.POST.get('slug')
        m.description = request.POST.get('description')
        m.price = request.POST.get('price')
        m.stock = request.POST.get('stock')
        m.is_avilable = request.POST.get('is_avilable') == 'on'
        m.category_id = request.POST.get('category')
        m.sku = request.POST.get('sku')
        m.priority = request.POST.get('priority')
        cat_image = request.FILES.get('images')

        if cat_image:
            if m.images:
                default_storage.delete(m.images.name)
            m.images = cat_image

        m.save()
        return redirect('allproduct')
    
    s=product.objects.filter(id=product_id)
    return render(request,'editproduct.html', {'m':s, 'categories': categories})
