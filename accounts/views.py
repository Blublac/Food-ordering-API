from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.decorators import api_view,authentication_classes,permission_classes

from accounts.models import IsSuperUser
from .serializers import Adminserializer, Changepasswordserializer, CustomUserserializer,CustomerLoginserializer
from django.contrib.auth import get_user_model,authenticate
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.signals import user_logged_in

User = get_user_model()


#admin account creation section, only the superuser can create an admin account
@swagger_auto_schema(methods=["POST"],request_body=Adminserializer())
@api_view(["POST"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsSuperUser])
def staff(request):
    if request.method  == "POST":
        serializer = Adminserializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["password"]=make_password(serializer.validated_data["password"])
            useradmin_data = User.objects.create(**serializer.validated_data)
            useradmin = Adminserializer(useradmin_data)
            data ={
                "status":True,
                "message":"created",
                "data":useradmin.data
            }
            return Response(data,status=status.HTTP_201_CREATED)
        else:
            error = {
                "status": False,
                "error":serializer.errors
            }
            return Response (error,status= status.HTTP_400_BAD_REQUEST)



#signup section for customers to signup
@swagger_auto_schema(methods=["POST"],request_body=CustomUserserializer())
@api_view (["POST"])
def signup_as_customer(request):
    if request.method =="POST":
        serializer = CustomUserserializer(data = request.data)
        if serializer.is_valid():
            serializer.validated_data["password"]=make_password(serializer.validated_data["password"])
            user = User.objects.create(**serializer.validated_data)
            user_serializer = CustomUserserializer(user)


            data={
                "status": True,
                "message":"created",

                "data":user_serializer.data
            }
            return Response(data,status=status.HTTP_201_CREATED)

        else:
            error = {
                "status": False,
                "error":serializer.errors
            }
            return Response (error,status= status.HTTP_400_BAD_REQUEST)
            
            
#this is the login section for all users
@swagger_auto_schema(methods=(["POST"]),request_body=CustomerLoginserializer())
@api_view(["POST"])
def customerlogin(request):
    if request.method == "POST":
        serializer = CustomerLoginserializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(request,email=serializer.validated_data["email"],password = serializer.validated_data["password"])
            if user:
                if user.is_active:
                    user_logged_in.send(sender=user.__class__,request=request,user=user)
                    log_serializer = CustomUserserializer(user)
                    data={
                        'status':True,
                        'message':'login successful',
                        'data':log_serializer.data
                    }
                    return Response(data,status=status.HTTP_202_ACCEPTED)
                
                else:
                    data={
                        'status':False,
                        'message':'Kindly activate your account'
                    }
                    return Response(data,status=status.HTTP_400_BAD_REQUEST)

            else:
                data={
                        'status':False,
                        'message':'Please enter a valid email and password'
                }
                return Response(data,status=status.HTTP_400_BAD_REQUEST)
        else:
            error={
                    'error':serializer.errors
            }
            return Response(error,status=status.HTTP_401_UNAUTHORIZED)






#get all customers,only a superuser is permitted
@api_view(["GET",])
@authentication_classes([BasicAuthentication])
@permission_classes([IsSuperUser])
def get_customers(request):
    if request.method =="GET":
        all_users = User.objects.all()
        serializer = CustomUserserializer(all_users,many = True)
        data={
            "status":True,
            "message":"success",
            "data": serializer.data
        }
        return Response (data,status=status.HTTP_200_OK)




#customers can get their details also update
@swagger_auto_schema(methods=(["PATCH","DELETE"]),request_body=CustomUserserializer())
@api_view(["GET","PATCH","DELETE"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def customer_details(request):
    try:
        usersdetails = User.objects.get(id=request.user.id,is_active=True,)
        if usersdetails.is_staff == True:
            data = {
            "message": "failed",
            "error": "You do not have the permission to view staff details"
            }
            return Response(data,status.HTTP_404_NOT_FOUND)
    
    
    except User.DoesNotExist:
            data = {
            "message": "failed",
            "error": "You have to login to view your details"
            }
            return Response(data,status.HTTP_404_NOT_FOUND)
    
    
    
    
    if request.method =="GET":
        serializer = CustomUserserializer(usersdetails)
        data={
            "status":True,
            "message":"success",
            "data": serializer.data
        }
        return Response (data,status=status.HTTP_200_OK)

    elif request.method == "PATCH":
        serializer = CustomUserserializer(usersdetails, data=request.data, partial =True)
        if serializer.is_valid():
            if "password" in serializer.validated_data.keys():
                error = {
                    "status":False,
                    "message": "password change not allowed here",
                    "data":serializer.errors
                }
                return Response(error,status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            data={
                "status": True,
                "message": "successful",
                "data": serializer.data
            }
            return Response(data,status=status.HTTP_202_ACCEPTED)
        else:
            error = {
                'message':'failed',
                'errors': serializer.errors
            }
            return Response(error,status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        usersdetails.delete()
        data={
            "status":True,
            "message": "Deleted"
        }
        return Response (data,status=status.HTTP_204_NO_CONTENT)





"""this is where admin can deactivate a user"""
@swagger_auto_schema(methods=(["DELETE"]),request_body=CustomUserserializer())
@api_view(["GET","DELETE"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsSuperUser])
def details(request,user):
    try:
        userdetails = User.objects.get(id=user,is_active =True)
    except User.DoesNotExist:
        data = {
        "message": "failed",
        "error": "user does not exist"
        }
        return Response(data,status.HTTP_404_NOT_FOUND)
    
    if request.method =="GET":

        serializer = CustomUserserializer(userdetails)
        data={
            "status":True,
            "message":"success",
            "data": serializer.data
        }
        return Response (data,status=status.HTTP_200_OK)

    elif request.method == "DELETE":
        userdetails.delete()
        data={
            "status":True,
            "message": "Deleted"
        }
        return Response (data,status=status.HTTP_204_NO_CONTENT)
@swagger_auto_schema(methods=['POST'],request_body=Changepasswordserializer())
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def change_password (request):
    user = request.user
    serializer = Changepasswordserializer(data=request.data)
    if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            if check_password(old_password, user.password):
                if serializer.validated_data['new_password']==serializer.validated_data['re_password']:

                    user.set_password(serializer.validated_data['new_password'])
                    
                    user.save()
                    
                    # print(user.password)
                    return Response({"message":"success"}, status=status.HTTP_200_OK)
                else:
                    error = {
                    'message':'failed',
                    "errors":"password does not match"
                }
        
                return Response(error, status=status.HTTP_400_BAD_REQUEST) 
                
            else:
                error = {
                'message':'failed',
                "errors":"Old password not correct"
            }
    
            return Response(error, status=status.HTTP_400_BAD_REQUEST) 