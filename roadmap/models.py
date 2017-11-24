from django.db import models
# Create your models here.

class Location(models.Model):
    category = models.CharField(max_length=200)
    dataset = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    phone = models.CharField(max_length=200)
    website = models.CharField(max_length=200)
    note = models.CharField(max_length=400)
    update_time = models.DateTimeField('update time')
    # user_ratings = ListField()
    # user_comments = ListField()

class Wifi(models.Model):
    organization = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
