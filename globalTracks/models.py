from django.db import models

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    totalconfirmed = models.IntegerField(default=0)
    totaldeaths = models.IntegerField(default=0)
    totalrecovered = models.IntegerField(default=0)
    latitude = models.DecimalField(max_digits=5, decimal_places=2)
    longitude = models.DecimalField(max_digits=5, decimal_places=2)
    lastupdate = models.CharField(max_length=100)

    def __str__(self):
        res = self.name[0]+self.name[1]+str(self.totalrecovered)+str(self.totaldeaths)
        return res

class Province(models.Model):
    name = models.CharField(max_length=100)
    totalconfirmed = models.IntegerField(default=0)
    totaldeaths = models.IntegerField(default=0)
    totalrecovered = models.IntegerField(default=0)
    latitude = models.DecimalField(max_digits=5, decimal_places=2)
    longitude = models.DecimalField(max_digits=5, decimal_places=2)
    country = models.ForeignKey(Country,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    totalconfirmed = models.IntegerField(default=0)
    totaldeaths = models.IntegerField(default=0)
    totalrecovered = models.IntegerField(default=0)
    latitude = models.DecimalField(max_digits=5, decimal_places=2)
    longitude = models.DecimalField(max_digits=5, decimal_places=2)
    keyid = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    country = models.ForeignKey(Country,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ImpParam(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.key
