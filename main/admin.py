from django.contrib import admin
from .models import Category,Food, Subcategory

@admin.register(Category)

class categoryadmin(admin.ModelAdmin):
    list_display=["category"]
    search_fields = ['category']


@admin.register(Subcategory)

class categoryadmin(admin.ModelAdmin):
    list_display=['subcategory',"category"]
    search_fields = ['category''subcategory']

@admin.register(Food)

class Foodadmin(admin.ModelAdmin):
    list_display=["food","subcategory"]
    search_fields = ['food']

