from . import views
from django.urls import path



urlpatterns=[
    path('categories',views.category),
    path('subcategories',views.subcategory),
    path('dishes',views.dishes),
]