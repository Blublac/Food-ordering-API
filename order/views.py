from django.core.exceptions import PermissionDenied, ValidationError
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

from order import serializers

User = get_user_model()



@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsSuperUser])
def orders (request):
    if request.method == 'GET':
        orderlist = Order.objects.values_list('status',flat=True).distinct()
        data = {
            orderlist:{
                'count':Order.objects.filter(status=orderlist).count(),
                'data':Order.objects.filter(status=orderlist).values()
                } for orderlist in orderlist
        }

        return Response(data,status.HTTP_200_OK)


#this is to place an order
@swagger_auto_schema(methods=["POST"],request_body=Orderserializer())
@api_view (["POST"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def place_order(request):

    if request.method =="POST":
        serializer = Orderserializer(data =request.data)
        if serializer.is_valid():
            if 'user' in serializer.validated_data.keys():
                serializer.validated_data.pop('user')


         
            orders = Order.objects.create(**serializer.validated_data,user = request.user)
            orders_serializer = Orderserializer(orders)

            data={
                "status": True,
                "message":"created",

                "data":orders_serializer.data
            }
            return Response(data,status=status.HTTP_201_CREATED)
        
        else:
            error={
                'status':False,
                "error": serializer.errors
            }
            return Response (error,status=status.HTTP_400_BAD_REQUEST)
    


@api_view (["GET"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def order_scheduled(request,order):
    if request.method == 'GET':
        try:
            schedule = Order.objects.get(order_no = order)
        except Order.DoesNotExist:
            data = {
            "message": "failed",
            "error": "Order with this order number does not exist"
            }
            return Response(data,status.HTTP_404_NOT_FOUND)


        if schedule.status == "pending":
            schedule.status = "scheduled"
            schedule.save()

            data = {
                'status': True,
                'message': 'order scheduled'
            }
            return Response(data,status.HTTP_202_ACCEPTED)

        else:
            data = {
                'status': False,
                'data': 'already scheduled'
            }
            return Response(data,status.HTTP_202_ACCEPTED)



@api_view (["GET"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def order_delivered(request,order):
    if request.method == 'GET':
        try:
            schedule = Order.objects.get(order_no = order)
        except Order.DoesNotExist:
            data = {
            "message": "failed",
            "error": "Order with this order number does not exist"
            }
            return Response(data,status.HTTP_404_NOT_FOUND)

        if schedule.status == "scheduled":
            schedule.status = "delivered"
            schedule.is_completed = True
            schedule.save()

            data = {
                'status': True,
                'message': 'order delivered'
            }
            return Response(data,status.HTTP_202_ACCEPTED)

        elif schedule.status == "pending":

            data = {
                'status': False,
                'message': 'this order is yet to be scheduled'
            }
            return Response(data,status.HTTP_403_FORBIDDEN)


        
        else:
            data = {
                'status': False,
                'data': 'already delivered'
            }
            return Response(data,status.HTTP_202_ACCEPTED)


@api_view (["GET"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def order_failed(request,order):
    if request.method == 'GET':
        try:
            schedule = Order.objects.get(order_no = order)
        except Order.DoesNotExist:
            data = {
            "message": "failed",
            "error": "Order with this order number does not exist"
            }
            return Response(data,status.HTTP_404_NOT_FOUND)

        if schedule.status == "scheduled":
            schedule.status = "failed"
            schedule.is_completed = True
            schedule.save()

            data = {
                'status': True,
                'message': 'delivery failed'
            }
            return Response(data,status.HTTP_202_ACCEPTED)

        elif schedule.status == "pending":

            data = {
                'status': False,
                'message': 'this order is yet to be scheduled'
            }
            return Response(data,status.HTTP_403_FORBIDDEN)


        elif schedule.status == "delivered":

            data = {
                'status': False,
                'message': 'this order  has been delivered'
            }
            return Response(data,status.HTTP_403_FORBIDDEN)
        
        else:
            data = {
                'status': False,
                'data': 'cancelled'
            }
            return Response(data,status.HTTP_202_ACCEPTED)



@api_view (["GET"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def order_cancelled(request,order):
    if request.method == 'GET':
        try:
            schedule = Order.objects.get(order_no = order)
        except Order.DoesNotExist:
            data = {
            "message": "failed",
            "error": "Order with this order number does not exist"
            }
            return Response(data,status.HTTP_404_NOT_FOUND)

        if schedule.status == "pending":
            schedule.status = "cancelled"
            schedule.is_completed = True
            schedule.save()

            data = {
                'status': True,
                'message': 'order cancelled'
            }
            return Response(data,status.HTTP_202_ACCEPTED)

        else:
            error = {
                'status': False,
                'data': 'pleas contact admin to assist you further'
            }
            return Response(error,status.HTTP_202_ACCEPTED)




@api_view (["GET"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def completed_orders(request):
    if request.method == 'GET':
        
        completed = Order.objects.filter(user = request.user, is_completed= True)

        serializer = Orderserializer(completed,many =True)
        data = {
                'status': True,
                'message': 'success',
                'data' : serializer.data
        }
        return Response(data,status.HTTP_202_ACCEPTED)




@api_view (["GET"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def all_user_orders(request):
    if request.method == 'GET':        

        orderlist = Order.objects.filter(user=request.user).values_list('status',flat=True).distinct()
        data = {
            orderlist:{
                'count':Order.objects.filter(status=orderlist).count(),
                'data':Order.objects.filter(status=orderlist).values()
                } for orderlist in orderlist
        }

        return Response(data,status.HTTP_200_OK)