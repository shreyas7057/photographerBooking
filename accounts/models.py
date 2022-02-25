from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self,email,full_name,password,**extra_fields):
        if not email:
            raise ValueError("You must provide email Address")

        email = self.normalize_email(email)
        user = self.model(email=email,full_name=full_name,**extra_fields)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,password,full_name,**other_fields):
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_photographer',False)
        other_fields.setdefault('is_active',True)
        other_fields.setdefault('is_superuser',True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser should have is_staff True')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser should have is_superuser True')

        return self.create_user(email,full_name,password,**other_fields)


class User(AbstractBaseUser,PermissionsMixin):
    USER_TYPE = (
        (1,'Admin'),
        (2,'Photographer'),
    )
    user_type = models.CharField(max_length=100,choices=USER_TYPE,default=2)
    email = models.EmailField(_("Email Id"),unique=True)
    full_name = models.CharField(_("Full Name"),max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_photographer = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    objests = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name',]
    

    def __str__(self):
        return self.email

    