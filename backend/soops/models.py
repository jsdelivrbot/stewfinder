from django.db import models
from vote.models import VoteModel

# Create your models here.


class Soop(VoteModel, models.Model):

    """this will be mapped into the SQL DB"""
    created = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=300,
                             blank=False,
                             null=False)

    details = models.CharField(max_length=3000,
                               # unique=True,
                               blank=False,
                               null=False)

    day = models.CharField(max_length=20,
                           blank=False,
                           null=False)

    outUrl = models.CharField(max_length=500,
                              unique=True,
                              blank=False,
                              null=False)

    food = models.CharField(max_length=500)

    when = models.CharField(max_length=75, null=True)

    location = models.CharField(max_length=500, null=True)

    score = models.FloatField(null=True, default=None)

    class Meta:
        ordering = ['created', ]
