from django.db import models

# Create your models here.

class sdetails(models.Model):
    symbol=models.CharField(max_length=150)
    price=models.FloatField(max_length=20)