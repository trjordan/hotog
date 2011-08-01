from django.db import models

# Create your models here.

class Place(models.Model):
    name = models.CharField(max_length=200)
    api_id = models.CharField(max_length=24, unique=True)

    def __unicode__(self):
        return self.name

class Visit(models.Model):
    place = models.ForeignKey(Place)
    date = models.DateField()
    api_id = models.CharField(max_length=24, unique=True)

    def __unicode__(self):
        return self.place.name + ' on ' + str(self.date)
