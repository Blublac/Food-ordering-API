from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.decorators import api_view,authentication_classes,permission_classes

from accounts.models import IsSuperUser
from main.models import Category, Food,Subcategory
from .serializers import FoodSerializer,CategorySerializer,SubCategorySerializer
from django.contrib.auth import get_user_model,authenticate
from drf_yasg.utils import swagger_auto_schema




@swagger_auto_schema(methods=(['POST']),request_body=CategorySerializer())
@api_view(['GET','POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsSuperUser])
def category (request):
    if request.method == 'GET':
        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories,many = True)
        data = {
            "status":True,
            "message": "successful",
            "data": serializer.data
        }
        return Response(data,status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = CategorySerializer(data = request.data)
        if serializer.is_valid():
            new_category =Category.objects.create(**serializer.validated_data)
            new_categoryserializer = CategorySerializer(new_category)
            data = {
                "status":True,
                "message": "created",
                "data": new_categoryserializer.data
            }
            return Response(data,status=status.HTTP_200_OK)
        else:

            error = {
                "status":False,
                "message": "failed to create category",
                "data": serializer.errors
            }
            return Response(error,status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=(['POST']),request_body=SubCategorySerializer())
@api_view(['GET','POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsSuperUser])
def subcategory (request):
    if request.method == 'GET':
        all_categories = Subcategory.objects.all()
        serializer = SubCategorySerializer(all_categories,many = True)
        data = {
            "status":True,
            "message": "successful",
            "data": serializer.data
        }
        return Response(data,status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = SubCategorySerializer(data = request.data)
        if serializer.is_valid():
            new_category =Subcategory.objects.create(**serializer.validated_data)
            new_categoryserializer = SubCategorySerializer(new_category)
            data = {
                "status":True,
                "message": "created",
                "data": new_categoryserializer.data
            }
            return Response(data,status=status.HTTP_200_OK)
        else:

            error = {
                "status":False,
                "message": "failed to create category",
                "data": serializer.errors
            }
            return Response(error,status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(methods=(['POST']),request_body=FoodSerializer())
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsSuperUser])
def dishes(request):
    if request.method == 'POST':
        serializer = FoodSerializer(data = request.data)
        if serializer.is_valid():
            new_category =Food.objects.create(**serializer.validated_data)
            new_categoryserializer = FoodSerializer(new_category)
            data = {
                "status":True,
                "message": "created",
                "data": new_categoryserializer.data
            }
            return Response(data,status=status.HTTP_200_OK)
        else:

            error = {
                "status":False,
                "message": "failed to create category",
                "data": serializer.errors
            }
            return Response(error,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def dishes_avaliable(request):
    if request.method == 'GET':
        all_categories = Food.objects.all()
        serializer =FoodSerializer(all_categories,many = True)
        data = {
            "status":True,
            "message": "successful",
            "data": serializer.data
        }
        return Response(data,status=status.HTTP_200_OK)


        


