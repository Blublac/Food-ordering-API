from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE
from accounts.models import CustomUser
import random

def generate_order_no():
    order_n = int(random.randint(3010000000, 3019999999))
    return order_n


class Orders(models.Model):
    user = models.ForeignKey (CustomUser,on_delete=CASCADE)
    order_no = models.IntegerField(default=generate_order_no,unique=True,editable=False)
    order = models.CharField(max_length=100)
    order_date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)

