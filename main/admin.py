from django.contrib import admin
from .models import Category,Food

@admin.register(Category)

class categoryadmin(admin.ModelAdmin):
    list_display=["category"]
    search_fields = ['category']


@admin.register(Food)

class Foodadmin(admin.ModelAdmin):
    list_display=["food"]
    search_fields = ['food']