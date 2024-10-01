from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserObjects (BaseUserManager): 

    def create_user(self, password, **fields) : 
        user = self.model(**fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, **fields) :
        fields['is_staff'] = True
        fields['is_superuser'] = True 
        return self.create_user(**fields)


class User (AbstractUser) : 
    objects = UserObjects()
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=225)
    balance = models.FloatField(default=0.0, null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self) -> str:
        return self.email