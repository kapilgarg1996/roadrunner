from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db.models import Q
from django.db import models, transaction
from django.db.utils import OperationalError
from runner.models import User
import urllib, urllib2
from datetime import datetime, timedelta
from django.utils import timezone
import json

def_bus_config = '1'
def_bus_config *= 56
def_ticket = '1'*56

PAYMENT_STATUS = (
        ('DONE', 'Done'),
        ('PENDING', 'Pending'),
        )

def get_drivers():
    return Q(post='Driver')
def get_conductors():
    return Q(post='Conductor')

def get_bus_file(instance, filename):
    return 'buses/bus_{0}/{1}'.format(instance.number, filename)

def get_employee_file(instance, filename):
    return 'employees/{0}/{1}/{2}_{3}'.format(instance.post, instance.shift, instance.name, filename)

def get_user_file(instance, filename):
    return 'users/{0}_{1}_{2}'.format(instance.name, instance.email, filename)

@python_2_unicode_compatible
class Bus(models.Model):
    id = models.AutoField(primary_key=True)  # Field name made lowercase.
    number = models.CharField(max_length=15, default='0')  # Field name made lowercase.
    ac = models.BooleanField(default=False)  # Field name made lowercase.
    seater = models.BooleanField(default=True)  # Field name made lowercase.
    total_seats = models.IntegerField(default='56')  # Field name made lowercase.
    fair_ratio = models.IntegerField(default=5)
    available = models.BooleanField(default=True)  # Field name made lowercase.
    image = models.ImageField(upload_to=get_bus_file, max_length=100, null=True)
    def __str__(self):
        return self.number

    class Meta:
        managed = True


@python_2_unicode_compatible
class Employee(models.Model):
    id = models.AutoField( primary_key=True)  # Field name made lowercase.
    name = models.CharField( max_length=100, default='')  # Field name made lowercase.
    shift = models.CharField( max_length=10, default='Morning')  # Field name made lowercase.
    post = models.CharField( max_length=10, default='Driver')  # Field name made lowercase.
    account = models.CharField( max_length=16, default='0')  # Field name made lowercase.
    contact = models.CharField( max_length=16, default='')
    address = models.CharField( max_length=100, default= '')
    image = models.ImageField( upload_to=get_employee_file, max_length='100', null=True)
    def __str__(self):
        return self.name+" ("+self.post+"-"+self.shift+")"

    class Meta:
        managed = True
        

@python_2_unicode_compatible
class Stop(models.Model):
    id = models.AutoField( primary_key=True)  # Field name made lowercase.
    name = models.CharField( max_length=100, default='')  # Field name made lowercase.
    city = models.CharField( max_length=100, default='')  # Field name made lowercase.
    state = models.CharField( max_length=100, default='')
    pincode = models.CharField( max_length=16, default='')
    def __str__(self):
        return self.name+"-"+self.city

    def get_location(self):
        return self.name+" "+self.city+" "+self.state+" "+self.pincode
    class Meta:
        managed = True

@python_2_unicode_compatible
class Route(models.Model):
    id = models.AutoField( primary_key=True)  # Field name made lowercase.
    source = models.ForeignKey(Stop, models.DO_NOTHING,  related_name='+')  # Field name made lowercase.
    dest = models.ForeignKey(Stop, models.DO_NOTHING,  related_name='+')  # Field name made lowercase.
    driver = models.ForeignKey(Employee, models.DO_NOTHING,  limit_choices_to=get_drivers, related_name='+')  # Field name made lowercase.
    conductor = models.ForeignKey(Employee, models.DO_NOTHING,  limit_choices_to=get_conductors, related_name='+')  # Field name made lowercase.
    bus = models.ForeignKey(Bus, models.DO_NOTHING,  related_name='+')  # Field name made lowercase.
    start_time = models.DateTimeField()  # Field name made lowercase.
    seats_avail = models.IntegerField(default='56')  # Field name made lowercase.
    seats_config = models.CharField(max_length=56, default=def_bus_config)
    journey_time = models.DateTimeField(null=True, blank=True)
    fair = models.IntegerField( null=True, default='0')
    def __str__(self):
        return str(self.source.name)+"("+str(self.source.city)+")"+"-"+str(self.dest.name)+"("+str(self.dest.city)+")"

    def save(self, *args, **kwargs):
        if(self.journey_time and self.fair):
            super(Route, self).save(*args, **kwargs)
        else:
            datadict = gmaps(source=self.source.get_location(), dest=self.dest.get_location())
            self.fair = self.bus.fair_ratio*datadict['distance']/1000
            self.journey_time = self.start_time + timedelta(seconds=datadict['time'])
            super(Route, self).save(*args, **kwargs)

    class Meta:
        managed = True 



@python_2_unicode_compatible
class Ticket(models.Model):
    id = models.AutoField( primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey(User, models.DO_NOTHING,  related_name='+')  # Field name made lowercase.
    route = models.ForeignKey(Route, models.DO_NOTHING,  related_name='+')  # Field name made lowercase.
    seats = models.IntegerField( default='0')  # Field name made lowercase.
    price = models.IntegerField( default='0')  # Field name made lowercase.
    book_time = models.DateTimeField()  # Field name made lowercase.
    seats_config = models.CharField(max_length=56, default=def_ticket)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS)
    def __str__(self):
        return self.user.name

    class Meta:
        managed = True
        

def gmaps(source='', dest=''):
    source = urllib.quote(source)
    dest = urllib.quote(dest)
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="+source+"&destinations="+dest+"&mode=driving&key=AIzaSyBg5U_b0snbOc3pWAadlcvYtRIEp9RpjK0"
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    data = response.read()

    datadict = json.loads(data)
    eldict = datadict['rows'][0]['elements'][0]
    distance = eldict['distance']['value']
    time = eldict['duration']['value']

    retdict = {}
    retdict['distance'] = distance
    retdict['time'] = time
    return retdict
