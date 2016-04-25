from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from taxi.models import *
from bus.models import *
from runner.models import *
from django.db import models

@python_2_unicode_compatible
class TaxiPayment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE)
    booking = models.ForeignKey(Booking, models.DO_NOTHING, null=True, blank=True)
    time = models.DateTimeField()
    token = models.CharField(max_length=200, db_index=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name

@python_2_unicode_compatible
class BusPayment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE)
    ticket = models.ForeignKey(Ticket, models.DO_NOTHING, null=True, blank=True)
    time = models.DateTimeField()
    token = models.CharField(max_length=200, db_index=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name

@python_2_unicode_compatible
class WalletTransaction(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE, null=True, blank=True)
    amount = models.IntegerField(default=0)
    time = models.DateTimeField()
    token = models.CharField(max_length=200, db_index=True)

    def __str__(self):
        return self.user.name
    
# Create your models here.
