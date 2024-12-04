from django.urls import path
from store import views
from common import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('addcategory', views.addcategory, name='addcategory'),
    path('allcategory', views.allcategory, name='allcategory'),
    path('deletecategory/<int:category_id>/', views.deletecategory, name='deletecategory'),
    path('editcategory/<int:category_id>/', views.editcategory, name='editcategory'),
    path('addproduct', views.addproduct, name='addproduct'),
    path('allproduct', views.allproduct, name='allproduct'),
    path('deleteproduct/<int:product_id>/', views.deleteproduct, name='deleteproduct'),
    path('editproduct/<int:product_id>/', views.editproduct, name='editproduct'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
