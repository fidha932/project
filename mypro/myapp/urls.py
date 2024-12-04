from django.urls import path
from myapp import views
from django.conf import settings

urlpatterns = [
    path('',views.home,name='home'),
    path('register',views.register,name='register'),
    path('log',views.log,name='log'),
    path('register_customer',views.register_customer,name='register_customer'),
    path('customerdashboard',views.customerdashboard,name='customerdashboard'),
    path('afterlogin',views.afterlogin,name='afterlogin'),
    path('register_admin',views.register_admin,name='register_admin'),
    path('logincustomer',views.logincustomer,name='logincustomer'),
    path('is_admin',views.is_admin,name='is_admin'),
    path('is_customer',views.is_customer,name='is_customer'),
    path('customerdashboard',views.customerdashboard,name='customerdashboard'),
    path('admindashboard',views.admindashboard,name='admindashboard'),
    path('logouts',views.logouts,name='logouts'),
    path('loginadmin',views.loginadmin,name='loginadmin'),

]
