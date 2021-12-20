from . import views
from django.urls import path



urlpatterns=[
    path('categories',views.category),
    path('subcategories',views.subcategory),
    path('dishes',views.dishes),
    path('dishes/all dishes',views.dishes_avaliable),
    #path('find dish/<str:item>',views.search_dish),
]