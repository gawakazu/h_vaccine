from django.db import models
from django.contrib.auth.models import AbstractUser

class PlaceModel(models.Model):
    place = models.CharField(max_length=50)
    def __str__(self):
        return self.place

class DateModel(models.Model):
    date = models.CharField(max_length=50)
    def __str__(self):
        return self.date

class TimeModel(models.Model):
    time = models.CharField(max_length=50)
    def __str__(self):
        return self.time

class CustomUser(AbstractUser,models.Model):
    class Meta(AbstractUser.Meta):
        pass
    address = models.CharField(max_length=50)
    def __str__(self):
        return self.username


class RegisterModel(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    place = models.ForeignKey(PlaceModel,on_delete=models.CASCADE)
    date = models.ForeignKey(DateModel,on_delete=models.CASCADE)
    time = models.ForeignKey(TimeModel,on_delete=models.CASCADE) 




