from django.db import models
from django.contrib.auth.models import User
from brand.models import Brand


# Create your models here.
class Car(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    details = models.TextField()
    quantity = models.IntegerField(default=1)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='cars') #one bra
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)

    
    def __str__(self):
        return self.title
    

class Comment(models.Model):
    post = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=30)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comments by : {self.name}"