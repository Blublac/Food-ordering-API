from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Vendor


User = get_user_model()

class CustomUserserializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["first_name","last_name","username","password","email","id","address","date_joined","last_login",]



class Vendorserializer(serializers.ModelSerializer):

    class Meta:
        model =Vendor
        fields = ["first_name","last_name","password","email","vendor_id","kitchen_name","kitchen_address","date_joined","last_login"]