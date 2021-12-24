from . import views
from django.urls import path


urlpatterns=[
    path('signup/staff',views.staff),
    path('signup/customer',views.signup_as_customer),
    path("login/customer",views.customerlogin),
    path("users/customers",views.get_customers),
    path("users/customer_details",views.customer_details),
    path("users/<uuid:user>",views.details),
    path("users/change password",views.change_password),
    # path("login/vendor",views.vendorlogin),
    # path('signup/vendor',views.signup_as_vendor),
    # path("users/vendors",views.get_vendors),
    # path("users/vendor_details",views.vendor_details),

]
