from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager


# Create your models here.
class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    activation_key = models.CharField(unique=True)
    activation_key_expires = models.DateTimeField(null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email
