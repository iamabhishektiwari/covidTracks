from django.db import models
from datetime import datetime

# Create your models here.



class States(models.Model):
    name = models.CharField(max_length=100, unique=True)
    totalconfirmed = models.IntegerField(default=0)
    totaldeaths = models.IntegerField(default=0)
    totalrecovered = models.IntegerField(default=0)
    latitude = models.DecimalField(max_digits=5, decimal_places=2)
    longitude = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class ImpParam(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.key
