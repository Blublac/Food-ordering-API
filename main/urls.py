from . import views
from django.urls import path



urlpatterns=[
    path('categories',views.category),
    path('dishes',views.dishes),
]