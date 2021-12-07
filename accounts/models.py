from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.
class CustomUser(AbstractUser):
    address = models.TextField()
    id = models.UUIDField(primary_key=True,unique=True,editable=False,default=uuid.uuid4)

    def __str__(self):
        return self.id


class Vendor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=16,default="PASSWORD MUST NOT BE MORE THAN 16")
    vendor_id = models.UUIDField(primary_key=True,unique=True,editable=False,default=uuid.uuid4)
    kitchen_name = models.CharField(max_length=100,unique=True)
    kitchen_address = models.TextField()
    date_joined = models.DateTimeField(auto_now=True)
    last_login= models.DateTimeField(auto_now_add=True)

    

 