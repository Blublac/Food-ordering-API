from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.fields import ReadOnlyField
from .models import Order


User = get_user_model()

class Orderserializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['order','name','billing_address','unit','order_no',]