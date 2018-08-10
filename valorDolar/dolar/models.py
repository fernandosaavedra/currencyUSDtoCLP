from django.db import models

class Dolar(models.Model):
    date = models.CharField(max_length=8)
    value = models.DecimalField(max_digits=7, decimal_places=2)
