from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager

class UserAccountManager(BaseUserManager):
    def create_user(self, email,name, password=None):
        if(not email):
            raise ValueError('Users must have a email address')

        email= self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save()

        return user

class UserAccount(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=9)
    height = models.FloatField(null=True,blank=True, default=None)
    width = models.FloatField(null=True,blank=True, default=None)
    x = models.FloatField(null=True,blank=True, default=None)
    y =models.FloatField(null=True,blank=True, default=None)
    unit = models.CharField(max_length=255, default='px')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserAccountManager()

    USERNAME_FIELD ='email'
    REQUIRED_FIELDS= ['name']

# Create your models here.
    def get_full_name(self):
        return self.name
    def get_short_name(self):
        return self.name
    def _str_(self):
        return self.email
