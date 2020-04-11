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

class State_k(models.Model):
    name = models.CharField(max_length=100, unique=True)
    confirmed = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    recovered = models.IntegerField(default=0)
    active = models.IntegerField(default=0)
    deltaConfirmed= models.IntegerField(default=0)
    deltaDeaths= models.IntegerField(default=0)
    deltaRecovered= models.IntegerField(default=0)
    lastupdate = models.CharField(max_length=200,default="Now")
    district_present = models.BooleanField(default=False)
    statecode = models.CharField(max_length=100, default='none')

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=100)
    confirmed = models.IntegerField(default=0)
    deltaConfirmed = models.IntegerField(default=0)
    state = models.ForeignKey(State_k,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class ImpParam(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.key
