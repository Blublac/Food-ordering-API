from . import views
from django.urls import path



urlpatterns=[
    path('order',views.orders),
    path('order/order',views.place_order),
    path('order/schedule<int:order>',views.order_scheduled),
    path('order/delivered<int:order>',views.order_delivered),
    path('order/failed<int:order>',views.order_failed),
]