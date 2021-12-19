from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
import uuid

class Category(models.Model):
    category = models.CharField(max_length=100,primary_key=True,unique=True)

    class Meta:
        verbose_name = 'catergory'
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.category
class Subcategory (models.Model):
    category = models.ForeignKey(Category,max_length=100,on_delete=CASCADE)
    subcategory = models.CharField(max_length=50,primary_key=True,unique=True)
    details = models.TextField()

    class Meta:
        verbose_name = 'Subcatergory'
        verbose_name_plural = "SubCategories"
    
    def __str__(self):
        return self.subcategory
class Food(models.Model):
    subcategory = models.ForeignKey(Subcategory,on_delete=CASCADE)
    sku_no = models.UUIDField(default=uuid.uuid4,unique=True,editable=False)
    food = models.CharField(primary_key= True,max_length=100,unique=True)
    price = models.PositiveBigIntegerField(null=True,blank=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField()



    class Meta:
        verbose_name = 'Food'
        verbose_name_plural = "Foods"



    def __str__(self):
        return f"{self.food},{self.price}"


    
    def delete(self):
        self.is_active = False
        self.save()
        return