from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from accounts.models import IsSuperUser
from .models import Order
from .serializers import Orderserializer
from django.contrib.auth import get_user_model,authenticate
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import make_password
from django.contrib.auth.signals import user_logged_in

User = get_user_model()

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsSuperUser])
def orders (request):
    if request.method == 'GET':
        all_orders = Order.objects.all(is_active = True)
        serializer = Orderserializer(all_orders)
        data = {
            "status":True,
            "message": "successful",
            "data": serializer.data
        }
        return Response(data,status=status.HTTP_200_OK)
