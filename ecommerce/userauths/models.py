from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True,null=False)
    username = models.CharField(max_length=100)
    bio = models.CharField(max_length=100)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __self__(self):
        return self.username
    # title = models.CharField()
    # desc = models.TextField()