from django.db import models

# Create your models here.

class Place(models.Model):
    name = models.CharField(max_length=200)

class Visit(models.Model):
    place = models.ForeignKey(Place)
    date = models.DateField()
