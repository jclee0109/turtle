import os

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from accountapp.models import User


def get_profile_image_upload_path(instance, filename):
    return os.path.join(
        "profiles", "user_%s" % instance.user_id, "%s" % filename)


class Profile(models.Model):
    profile_id = models.BigAutoField(primary_key=True)
    img = models.ImageField(upload_to=get_profile_image_upload_path)

    nickname = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)