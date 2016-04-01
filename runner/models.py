# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#""""
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db.models import Q
from django.db import models, transaction
from django.db.utils import OperationalError

def get_user_file(instance, filename):
    return 'users/{0}_{1}_{2}'.format(instance.name, instance.email, filename)
"""
def_bus_config = '1'
def_bus_config *= 56
def_ticket = '0'*56
DRIVER = ()
CONDUCTOR = ()

def get_drivers():
    return Q(post='Driver')
def get_conductors():
    return Q(post='Conductor')

def get_bus_file(instance, filename):
    return 'buses/bus_{0}/{1}'.format(instance.number, filename)

def get_employee_file(instance, filename):
    return 'employees/{0}/{1}/{2}_{3}'.format(instance.post, instance.shift, instance.name, filename)


@python_2_unicode_compatible
class Bus(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    number = models.CharField(db_column='NUMBER', max_length=15, default='0')  # Field name made lowercase.
    ac = models.BooleanField(db_column='AC', default=False)  # Field name made lowercase.
    seater = models.BooleanField(db_column='SEATER', default=True)  # Field name made lowercase.
    total_seats = models.IntegerField(db_column='TOTAL_SEATS', default='56')  # Field name made lowercase.
    available = models.BooleanField(db_column='AVAILABLE', default=True)  # Field name made lowercase.
    image = models.ImageField(db_column='IMAGE', upload_to=get_bus_file, max_length=100, null=True)
    def __str__(self):
        return self.number

    class Meta:
        managed = True
        db_table = 'Bus'


@python_2_unicode_compatible
class Employee(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=100, default='')  # Field name made lowercase.
    shift = models.CharField(db_column='SHIFT', max_length=10, default='Morning')  # Field name made lowercase.
    post = models.CharField(db_column='POST', max_length=10, default='Driver')  # Field name made lowercase.
    account = models.CharField(db_column='ACCOUNT', max_length=16, default='0')  # Field name made lowercase.
    contact = models.CharField(db_column='CONTACT', max_length=16, default='')
    address = models.CharField(db_column='ADDRESS', max_length=100, default= '')
    image = models.ImageField(db_column='IMAGE', upload_to=get_employee_file, max_length='100', null=True)
    def __str__(self):
        return self.name+" ("+self.post+"-"+self.shift+")"

    class Meta:
        managed = True
        db_table = 'Employee'


@python_2_unicode_compatible
class Route(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    source = models.ForeignKey('Stop', models.DO_NOTHING, db_column='SOURCE', related_name='+')  # Field name made lowercase.
    dest = models.ForeignKey('Stop', models.DO_NOTHING, db_column='DEST', related_name='+')  # Field name made lowercase.
    driver = models.ForeignKey(Employee, models.DO_NOTHING, db_column='DRIVER', limit_choices_to=get_drivers, related_name='+')  # Field name made lowercase.
    conductor = models.ForeignKey(Employee, models.DO_NOTHING, db_column='CONDUCTOR', limit_choices_to=get_conductors, related_name='+')  # Field name made lowercase.
    bus = models.ForeignKey(Bus, models.DO_NOTHING, db_column='BUS', related_name='+')  # Field name made lowercase.
    start_time = models.DateTimeField(db_column='START_TIME')  # Field name made lowercase.
    seats_avail = models.IntegerField(db_column='SEATS_AVAIL', default='56')  # Field name made lowercase.
    seats_config = models.CharField(db_column='SEATS_CONFIG', max_length=56, default=def_bus_config)
    journey_time = models.DateTimeField(db_column='JOURNEY_TIME')
    fair = models.IntegerField(db_column='FAIR', default='0')
    def __str__(self):
        return str(self.source.name)+"("+str(self.source.city)+")"+"-"+str(self.dest.name)+"("+str(self.dest.city)+")"


    class Meta:
        managed = True
        db_table = 'Route'


@python_2_unicode_compatible
class Stop(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=100, default='')  # Field name made lowercase.
    city = models.CharField(db_column='CITY', max_length=100, default='')  # Field name made lowercase.
    def __str__(self):
        return self.name+"-"+self.city

    class Meta:
        managed = True
        db_table = 'Stop'
"""



class UserAbstract(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, default=1)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=100, default='')  # Field name made lowercase.
    password = models.CharField(db_column='PASSWORD', max_length=20, default='')  # Field name made lowercase.
    credit_card = models.CharField(db_column='CREDIT_CARD', max_length=25, default='')  # Field name made lowercase.
    contact = models.CharField(db_column='CONTACT', blank=True, null=True, max_length=16)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=100, default='')  # Field name made lowercase.
    image = models.ImageField(db_column='IMAGE', max_length=100, upload_to=get_user_file, null=True)
    wallet = models.IntegerField(db_column='WALLET', default=0)
    
    def __str__(self):
        return self.name

    class Meta:
        abstract = True

@python_2_unicode_compatible
class User(UserAbstract):
    def __str__(self):
        return self.name ;
    class Meta:
        managed = True
        db_table = 'User'

"""
@python_2_unicode_compatible
class Ticket(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='USER', related_name='+')  # Field name made lowercase.
    route = models.ForeignKey(Route, models.DO_NOTHING, db_column='ROUTE', related_name='+')  # Field name made lowercase.
    seats = models.IntegerField(db_column='SEATS', default='0')  # Field name made lowercase.
    price = models.IntegerField(db_column='PRICE', default='0')  # Field name made lowercase.
    book_time = models.DateTimeField(db_column='BOOK_TIME')  # Field name made lowercase.
    seats_config = models.CharField(db_column='SEATS_CONFIG', max_length=56, default=def_ticket)
    def __str__(self):
        return self.user.name

    class Meta:
        managed = True
        db_table = 'Ticket'

"""
