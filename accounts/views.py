from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.decorators import api_view,authentication_classes,permission_classes

from accounts.models import IsSuperUser
from .serializers import Adminserializer, CustomUserserializer,CustomerLoginserializer
from django.contrib.auth import get_user_model,authenticate
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import make_password
from django.contrib.auth.signals import user_logged_in

User = get_user_model()


#admin account creation section
@swagger_auto_schema(methods=["POST"],request_body=Adminserializer())
@api_view(["POST"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
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


#signup section for customers and password hash
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






#get all customers
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


@api_view(["GET","DELETE"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def get_A_customers(request,user_id):
    try:
        user = User.objects.get(id=user_id,is_active=True)
    except User.DoesNotExist:
        raise ValidationError(message="invalid id")
    if request.method =="GET":
        serializer = CustomUserserializer(user)
        data={
            "status":True,
            "message":"success",
            "data": serializer.data
        }
        return Response (data,status=status.HTTP_200_OK)
    elif request.method == "DELETE":

        user.delete()
        data = {
            'message':'success'
        }





#customers can get their details also update
@swagger_auto_schema(methods=(["PATCH","DELETE"]),request_body=CustomUserserializer())
@api_view(["GET","PATCH","DELETE"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def customer_details(request):
    try:
        usersdetails = User.objects.get(id=request.user.id,is_active=True)
    except User.DoesNotExist:
        raise ValidationError(message="please login to view details")
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
                raise ValidationError(message="password cannot be changed from here")
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






# @swagger_auto_schema(methods=["POST"],request_body=Vendorserializer())
# @api_view(["POST"])
# def signup_as_vendor(request):
#     if request.method == "POST":
#         serializer = Vendorserializer(data = request.data)
#         if serializer.is_valid():
#             serializer.validated_data['password']=make_password(serializer.validated_data['password'])
#             vendor_data = Vendor.objects.create(**serializer.validated_data)
#             vendor = Vendorserializer(vendor_data)

#             data={
#                 "status": True,
#                 "message": "created",
#                 "data": vendor.data
#             }
#             return Response (data, status=status.HTTP_201_CREATED)



# @swagger_auto_schema(methods=(["POST"]),request_body=VendorLoginserializer())
# @api_view(["POST"])
# def vendorlogin(request):
#     if request.method == "POST":
#         serializer = VendorLoginserializer(data=request.data)
#         if serializer.is_valid():
#             user = Vendor.objects.get(email= serializer.validated_data["email"],password = serializer.validated_data["password"])
#             if user:
#                 if user:
#                     user_logged_in.send(sender=user.__class__,request=request,user=user)
#                     log_serializer = Vendorserializer(user)
#                     data={
#                         'status':True,
#                         'message':'login successful',
#                         'data':log_serializer.data
#                     }
#                     return Response(data,status=status.HTTP_202_ACCEPTED)
                
#                 else:
#                     data={
#                         'status':False,
#                         'message':'Kindly activate your account'
#                     }
#                     return Response(data,status=status.HTTP_400_BAD_REQUEST)

#             else:
#                 data={
#                         'status':False,
#                         'message':'Please enter a valid username and password'
#                 }
#                 return Response(data,status=status.HTTP_400_BAD_REQUEST)
#         else:
#             error={
#                     'error':serializer.errors
#             }
#             return Response(error,status=status.HTTP_401_UNAUTHORIZED)

# #get all vendors
# @api_view(["GET",])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAdminUser])
# def get_vendors(request):
#     if request.method =="GET":
#         all_vendors = User.objects.all()
#         serializer = Vendorserializer(all_vendors,many = True)
#         data={
#             "status":True,
#             "message":"success",
#             "data": serializer.data
#         }
#         return Response (data,status=status.HTTP_200_OK)




# #customers can get their details also update
# @swagger_auto_schema(methods=(["PATCH","DELETE"]),request_body=Vendorserializer())
# @api_view(["GET","PATCH","DELETE"])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])
# def vendor_details(request):
#     if request.method =="GET":
#         try:
#             vendordetails = User.objects.get(id=request.user.id,is_active =True)
#         except User.DoesNotExist:
#             data = {
#             "message": "failed",
#             "error": "user with iddoes not exist"
#         }
#         return Response(data,status.HTTP_404_NOT_FOUND)

#         serializer = Vendorserializer(vendordetails)
#         data={
#             "status":True,
#             "message":"success",
#             "data": serializer.data
#         }
#         return Response (data,status=status.HTTP_200_OK)







