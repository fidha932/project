from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .models import customerprofile
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
from common.models import *
from store.models import *
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    m=product.objects.all()
    return render(request,'home.html',{'m':m})

def register(request):
    return render(request,'allregister.html')

def log(request):
    return render(request,'all_login.html')

@csrf_exempt
def register_customer(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        gender = request.POST.get('gender')
        profile= request.FILES.get('profile')
        repassword=request.POST.get('repassword')
        if password==repassword:
            if User.objects.filter(username=username).exists():
                    messages.error(request, 'username exist')
            elif User.objects.filter(email=email).exists():
                    messages.error(request, 'Email exist')
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username, password=password, email=email)
            customer=customerprofile.objects.create(
                user=user,
                phone_number=phone_number,
                address=address,
                city=city,
                state=state,
                gender=gender,
                profile=profile
            )    
            customer.save()
            customer_group = Group.objects.get_or_create(name='CUSTOMER')
            customer_group[0].user_set.add(user)
            messages.success(request, 'Account created successfully! Please check your email for activate the account .')  
            return redirect('log')         
        else:
            messages.success(request, 'please..check registration is failed')           
    return render(request, 'registercustomer.html')


def register_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if password==repassword:
            if User.objects.filter(username=username).exists():
                    messages.error(request,'username exist')
            elif User.objects.filter(email=email).exists():
                    messages.error(request,'Email exist')
                    
            user=User.objects.create(
                        username=username,
                        email=email,
                        first_name=first_name,
                        last_name=last_name
            )
                    
            user.set_password(password)
            user.save()
            
            my_admin_group, created = Group.objects.get_or_create(name='SELLER')
            my_admin_group.user_set.add(user)
            return redirect('log')
        else:
            messages.info(request,'password donot match')
    return render(request,'registeradmin.html')
        
def logincustomer(request):
       if request.user.is_authenticated:
          if request.user.groups.filter(name='CUSTOMER'):
             return HttpResponseRedirect('customerdashboard')
        
       if request.method=='POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(request,username=username,password=password)
            if user is not None:
                if user.groups.filter(name='CUSTOMER').exists():
                 login(request,user)
                 return redirect('afterlogin')
       return render(request,'logincustomer.html')


def afterlogin(request):
    if is_admin(request.user):
        return redirect('admindashboard')
    elif is_customer(request.user):
        if customerprofile.objects.filter(user_id=request.user.id).first():
            return redirect('customerdashboard') 


def is_admin(user):
    return user.groups.filter(name='SELLER').exists()

def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()



def customerdashboard(request):
    if not request.user.is_authenticated:
        return redirect('logincustomer')  # Redirect the user to the login page if not authenticated

    customer_profile = get_object_or_404(customerprofile, user=request.user)
    return render(request, 'customerdashboard.html', {'profile': customer_profile})

def admindashboard(request):
    return render(request,'admindashboard.html')

def logouts(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')

def loginadmin(request):
       if request.user.is_authenticated:
          if request.user.groups.filter(name='SELLER'):
             return HttpResponseRedirect('admindashboard')
        
       if request.method=='POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(request,username=username,password=password)
            if user is not None:
                if user.groups.filter(name='SELLER').exists():
                 login(request,user)
                 return redirect('afterlogin')
       return render(request,'loginadmin.html')
