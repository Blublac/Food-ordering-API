from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from .serializers import CustomUserserializer, User,Vendorserializer
from .models import Vendor
from django.contrib.auth import get_user_model,authenticate
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import make_password


User = get_user_model()
#signup section for customers and password hash
@swagger_auto_schema(methods=["POST"],request_body=CustomUserserializer())
@api_view (["POST"])
def signup_as_customer(request):
    if request.method =="POST":
        serializer = CustomUserserializer(data = request.data)
        if serializer.is_valid():
            serializer.validated_data["password"]= make_password(serializer.validated_data["password"])
            user = User.objects.create(**serializer.validated_data)
            user_serializer = CustomUserserializer(user)

            data={
                "status": True,
                "message":"created",

                "data":user_serializer.data
            }
            return Response(data,status=status.HTTP_201_CREATED)


#signup section for vendors
@swagger_auto_schema(methods=["POST"],request_body=Vendorserializer())
@api_view(["POST"])
def signup_as_vendor(request):
    if request.method == "POST":
        serializer = Vendorserializer(data = request.data)
        if serializer.is_valid():
            serializer.validated_data['password']=make_password(serializer.validated_data['password'])
            vendor_data = Vendor.objects.create(**serializer.validated_data)
            vendor = Vendorserializer(vendor_data)

            data={
                "status": True,
                "message": "created",
                "data": vendor.data
            }
            return Response (data, status=status.HTTP_201_CREATED)
            

