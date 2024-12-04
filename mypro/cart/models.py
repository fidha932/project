from django.db import models
from store.models import product
from django.contrib.auth.models import User

# Create your models here.
class Cart(models.Model):
    cart_id=models.CharField(max_length=250, blank=True, null=False, unique=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_added=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    

class Cart_item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    Product=models.ForeignKey(product,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=1) 
    is_active=models.BooleanField(default=True)
    
    def sub_total(self):
       return self.Product.price*self.quantity
        
    def __str__(self):
        return self.Product.product_name
