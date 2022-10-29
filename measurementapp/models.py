from django.db import models

# Create your models here.
from jsonfield import JSONField

from profileapp.models import Profile


class Measurement(models.Model):
    measurement_id = models.BigAutoField(primary_key=True)

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    angles = models.JSONField(default=[])
    average_angle = models.FloatField(default=0)

    base_angle = models.FloatField(default=0)

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
