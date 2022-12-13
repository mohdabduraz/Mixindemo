from django.db import models

# Create your models here.

class UserDetails(models.Model):
    username = models.EmailField()
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    longitude = models.FloatField()
    latitude = models.FloatField()
    deviceName = models.CharField(max_length=200)
    date = models.DateField()
