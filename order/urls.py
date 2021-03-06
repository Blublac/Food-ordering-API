from . import views
from django.urls import path



urlpatterns=[
    path('order',views.orders),
    path('order/new',views.place_order),
    path('order/schedule<int:order>',views.order_scheduled),
    path('order/delivered<int:order>',views.order_delivered),
    path('order/failed<int:order>',views.order_failed),
    path('order/cancelled<int:order>',views.order_cancelled),
    path('order/completed',views.completed_orders),
    path('order/orders',views.all_user_orders),
]