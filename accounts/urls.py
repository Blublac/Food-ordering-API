from . import views
from django.urls import path


urlpatterns=[
    path('signup as customer',views.signup_as_customer),
    path('signup as vendor',views.signup_as_vendor),

]
