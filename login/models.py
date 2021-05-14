from django.db import models

# Create your models here.
class Registration(models.Model):
    name=models.CharField(max_length=60)
    username = models.CharField(max_length=25)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=16)
