from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Order


User = get_user_model()

class Orderserializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"