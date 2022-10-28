from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from accountapp.models import User


class Profile(models.Model):
    profile_id = models.BigAutoField(primary_key=True)
    img = models.CharField(max_length=700, null=True, blank=True)

    nickname = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)