from django.db import models
from django.db.models.deletion import DO_NOTHING
from accounts.models import CustomUser
import random

def generate_order_no():
    order_n = int(random.randint(3010000000, 3019999999))
    return order_n
# Create your models here.


class Order(models.Model):
    STATUS_CHOICES = (
       ("pending","Pending"),
        ("scheduled","Scheduled"),
        ("delivered","Delivered"),
        ("failed","Delivery Failed"),
        ("cancelled","Cancelled")
    )
    staus = models.CharField(max_length=50,choices=STATUS_CHOICES,default="pending")
    is_active = models.BooleanField()
    user = models.ForeignKey (CustomUser,on_delete=DO_NOTHING)
    order_no = models.IntegerField(primary_key=True,default=generate_order_no,unique=True,editable=False)
    unit = models.IntegerField(default=0)
    price = models.PositiveIntegerField()
    order = models.CharField(max_length=100)
    order_date = models.DateField(auto_now=True)
    completed = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)



    def __str__(self):
        return self.order_no