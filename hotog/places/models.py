from datetime import datetime

from django.db import models

# Create your models here.

class Place(models.Model):
    name = models.CharField(max_length=200)
    api_id = models.CharField(max_length=24, unique=True)

    def __unicode__(self):
        return self.name

class Visit(models.Model):
    place = models.ForeignKey(Place)
    date = models.DateTimeField()
    api_id = models.CharField(max_length=24, unique=True)

    def is_relevant(self):
        " Checks whether this visit was the same meal as now would be. "
        # Before 4PM is lunch, after 4PM is dinner
        return (self.date.hour < 16) == (datetime.now().hour < 16)

    def __unicode__(self):
        return self.place.name + ' on ' + str(self.date)
