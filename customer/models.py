from django.db import models
from django.contrib.auth.models import User
from car.models import Car

class PurchaseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} purchased {self.car.title} on {self.purchased_at}"
