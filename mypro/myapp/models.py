from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class customerprofile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=10)
    address=models.CharField(max_length=250)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    gender=models.CharField(max_length=1)
    profile=models.FileField(upload_to='media')
    old_cart=models.CharField(max_length=200,blank=True,null=True)
    def __str__(self):
        return self.user.username
    

    