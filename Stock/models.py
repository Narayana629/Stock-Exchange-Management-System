from django.db import models

# Create your models here.

class Profile(models.Model):
    first_name=models.CharField(max_length=60,null=True)
    last_name = models.CharField(max_length=25,null=True)
    email = models.CharField(max_length=50,null=True)
    gender=models.CharField(max_length=10,null=True)
    dateofbirth=models.DateField(null=True)
    phone=models.IntegerField(null=True)
    qualification=models.CharField(max_length=20,null=True)
    address1=models.CharField(max_length=60,null=True)
    address2=models.CharField(max_length=60,null=True)
    state = models.CharField(max_length=25,null=True)
    postcode = models.IntegerField(null=True)
    city = models.CharField(max_length=25,null=True)
    country = models.CharField(max_length=25,null=True)
    photo=models.ImageField(default='',null=True,blank=True,upload_to='')


class Buystock(models.Model):
    name=models.CharField(max_length=100)
    username=models.CharField(max_length=60)
    ticker = models.CharField(max_length=25,primary_key=True)
    quantity = models.IntegerField()
    datebought=models.DateField()
    price=models.FloatField()

class Activity(models.Model):
    name=models.CharField(max_length=100)
    type=models.CharField(max_length=10)
    quantity = models.IntegerField()
    datebought=models.DateField()
    username = models.CharField(max_length=60)

class Stockd(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=60)
    ticker = models.CharField(max_length=25, primary_key=True)
    quantity = models.IntegerField()
    datebought = models.DateField()
    price = models.FloatField()
    lastprice = models.FloatField()
    change = models.FloatField()
    type = models.CharField(max_length=60, null=True)
    profit = models.FloatField()

class Stbuy(models.Model):
    name = models.CharField(max_length=100)
    ticker = models.CharField(max_length=25, primary_key=True)
    price = models.FloatField(null=True)

class Wallet(models.Model):
    username = models.CharField(max_length=60)
    balance=models.FloatField(null=True)