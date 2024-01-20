from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(unique=False, max_length=50)
    email = models.CharField(unique=True, max_length=80)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    def __str__(self) -> str:
        return self.username
    
    