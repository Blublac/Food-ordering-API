
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import uuid

from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    """
    Allows access only to super users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)
class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4,unique=True)


    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


    def __unicode__(self):
        return self.email,self.name
    
    def delete(self):
        self.is_active = False
        self.save()
        return



# class Vendor(models.Model):
#     email = models.EmailField(max_length=254, unique=True)
#     name = models.CharField(max_length=254)
#     is_vendor = models.BooleanField(default=False)
#     vendor = models.CharField(max_length=100,unique=True,blank=True)
#     location = models.TextField()
#     is_active = models.BooleanField(default=True)
#     last_login = models.DateTimeField(null=True, blank=True)
#     date_joined = models.DateTimeField(auto_now_add=True)
#     id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4,unique=True)
