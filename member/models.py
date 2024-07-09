from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    REQUIRED_FIELDS = []
    email = None
    nickname = models.CharField(max_length=100)
    university = models.CharField(max_length=50)

class AccessUser(models.Model):
    username = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE, related_name='access_username')
    password = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE, related_name='access_userpassword')