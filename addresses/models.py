from django.db import models


class Address(models.Model):
    number = models.IntegerField()
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=55)
    state = models.CharField(max_length=2)
