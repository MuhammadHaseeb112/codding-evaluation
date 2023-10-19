from django.db import models

class MyModel(models.Model):
    date = models.DateField()
    distance = models.IntegerField()