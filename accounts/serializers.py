from rest_framework import serializers
#from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model

User = get_user_model()

#this serializer is to create different levels of admin account
class Adminserializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields =["name","password","email","date_joined","last_login","is_staff"]


#this serializer is to create regular user account 
class CustomUserserializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["name","password","email","date_joined","last_login",]


#vendor account serializer


#customer login serializer
class CustomerLoginserializer(serializers.Serializer):
    email = serializers.EmailField(max_length= 500)
    password = serializers.CharField(max_length =500)




# class Vendorserializer(serializers.ModelSerializer):

#     class Meta:
#         model = Vendor
#         fields = ["name","password","email","vendor","location","is_vendor","date_joined","last_login"]




# class VendorLoginserializer(serializers.Serializer):
#     vendor = serializers.CharField(max_length=100)
#     password = serializers.CharField(max_length =16)

