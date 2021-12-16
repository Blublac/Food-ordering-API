from django.db import models
from django.db.models.deletion import DO_NOTHING
from accounts.models import CustomUser
import random

from main.models import Food

def generate_order_no():
    order_n = int(random.randint(30000000, 39999999))
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
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default="pending")
    user = models.ForeignKey (CustomUser,on_delete=DO_NOTHING,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    order_no = models.IntegerField(primary_key=True,default=generate_order_no,unique=True,editable=False)
    unit = models.PositiveSmallIntegerField(default=1)
    order = models.ForeignKey(Food,max_length=100,on_delete=DO_NOTHING)
    name = models.CharField(max_length=50)
    billing_address =  models.TextField()
    time = models.TimeField(auto_now=True)
    order_date = models.DateField(auto_now=True)
    is_completed = models.BooleanField(default=False)
    updated = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = "Orders"


    def __unicode__(self):
        return self.order_no


    def getname(self):
        name = CustomUser.objects.filter(name=self)
        return name

    def getemail(self):
        email = CustomUser.objects.filter(email=self)
        return email
 