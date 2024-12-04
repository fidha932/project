from django.urls import path
from store import views

urlpatterns = [
    path('shop/', views.shop, name='shop'),  # For all products
    path('shop/<category_slug>/<product_slug>/', views.product_detail, name='product_detail'),

]