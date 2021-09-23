from django.db import models


# Create your models here.

class Fibonacci(models.Model):
    index = models.IntegerField()
    value = models.IntegerField()
