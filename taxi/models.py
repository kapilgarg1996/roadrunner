from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models, transaction
from runner.models import User
TAXI_TYPES = (
        ('SUV', 'SUV'),
        ('TRUCK', 'Truck'),
        ('SEDAN', 'Sedan'),
        ('VAN', 'Van'),
        ('WAGON', 'Wagon'),
        ('CONVERTIBLE', 'Convertible'),
        ('SPORTS', 'Sports'),
        ('DIESEL', 'Diesel'),
        ('CROSSOVER', 'Crossover'),
        ('LUXURY', 'Luxury'),
        ('ELECTRIC', 'Electric'),
        ('HATCHBACK', 'Hatchback'),
        ('OTHER', 'Other'),
)

PAYMENT_STATUS = (
        ('DONE', 'Successful'),
        ('PENDING', 'Later')
        )
def get_car_file(instance, filename):
    return 'taxis/taxi_{0}/{1}'.format(instance.number, filename)

def get_employee_file(instance, filename):
    return 'employees/{0}/{1}_{2}'.format("taxi_drivers", instance.name, filename)

@python_2_unicode_compatible
class Taxi(models.Model):
    id = models.AutoField(primary_key=True)  # Field name made lowercase.
    number = models.CharField(max_length=15, default='0')  # Field name made lowercase.
    ac = models.BooleanField(default=False)  # Field name made lowercase.
    total_seats = models.IntegerField(default='4')  # Field name made lowercase.
    taxi_type = models.CharField(max_length=20, choices = TAXI_TYPES)
    fair_ratio = models.IntegerField(default=10)
    taxi_info = models.CharField(max_length=200, null=True)
    available = models.BooleanField(default=True)  # Field name made lowercase.
    image = models.ImageField(upload_to=get_car_file, max_length=100, null=True)
    
    def __str__(self):
        return self.number

    class Meta:
        managed = True

@python_2_unicode_compatible
class Driver(models.Model):
    id = models.AutoField(primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=100, default='')  # Field name made lowercase.
    account = models.CharField(max_length=16, default='0')  # Field name made lowercase.
    contact = models.CharField(max_length=16, default='')
    address = models.CharField(max_length=100, default= '')
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to=get_employee_file, max_length='100', null=True)
    def __str__(self):
        return self.name

    class Meta:
        managed = True

@python_2_unicode_compatible
class Place(models.Model):
    id = models.AutoField(primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=100, default='')  # Field name made lowercase.
    city = models.CharField(max_length=100, default='')  # Field name made lowercase.
    state = models.CharField(max_length=100, default='')
    pincode = models.CharField(max_length=16, default='')
    
    def __str__(self):
        return self.name+"-"+self.city

    def get_location(self):
        return self.name+" "+self.city+" "+self.state+" "+self.pincode
    
    class Meta:
        managed = True

@python_2_unicode_compatible
class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING, related_name='+')
    taxi = models.ForeignKey(Taxi, models.DO_NOTHING, related_name='+')
    driver = models.ForeignKey(Driver, models.DO_NOTHING, related_name='+')
    source = models.ForeignKey(Place, models.DO_NOTHING, related_name='+')
    dest = models.ForeignKey(Place, models.DO_NOTHING, related_name='+')
    booking_time = models.DateTimeField()
    journey_time = models.DateTimeField()
    journey_endtime = models.DateTimeField()
    fair = models.IntegerField(default=0)
    payment_status = models.CharField(max_length=20,choices = PAYMENT_STATUS)

    def __str__(self):
        return self.user.name+" "+self.taxi.number
