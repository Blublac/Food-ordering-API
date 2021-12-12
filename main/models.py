from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE
import uuid

class Category(models.Model):
    category_choices=(
        ('Bakery',('cake','cookies','bread','pies','pizza')),
        ('rice',('jollof rice','fried rice','chinese rice','rice & stew','coconut rice')),
        ('roast',('corn','beans & roasted plantain','bole','roasted chicken')),
        ('barbeque',('grilled chicken','grilled beef','grilled fish','suya')),
        ('sharwarma',('chicken','beef','chicken jumbo+2hotdog','beef jumbo+2hotdog')),
    )
    
    category = models.CharField(max_length=100,null = True,blank=True,unique=True)
    subcategory = models.CharField(max_length=100,default=category_choices, unique=True)
    details = models.TextField()

    class Meta:
        verbose_name = 'catergory'
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.category



class Food(models.Model):
    category = models.ForeignKey(Category,on_delete=CASCADE)
    sku_no = models.UUIDField(primary_key= True, default=uuid.uuid4,unique=True,editable=False)
    food = models.CharField(max_length=100,unique=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField()



    class Meta:
        verbose_name = 'Food'
        verbose_name_plural = "Foods"



    def __str__(self):
        return self.food


    
    def delete(self):
        self.is_active = False
        self.save()
        return
    
