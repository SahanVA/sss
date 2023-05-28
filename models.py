from pyexpat import model
from django.db import models

class users(models.Model):
    name  = models.CharField(max_length=100)
    username  = models.CharField(max_length=100)
    password  = models.CharField(max_length=100)
    photo = models.CharField(max_length=20)
    status = models.CharField(max_length=2)
    level = models.CharField(max_length=100)
    class Meta:
        db_table='users'

class Cat(models.Model):
    name = models.CharField(max_length=30)
    picture = models.FileField(upload_to='')

