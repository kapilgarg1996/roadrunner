from django.contrib import admin
from taxi.models import *

class TaxiAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'ac', 'taxi_type', 'total_seats', 'available')

class DriverAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'contact', 'address')

class PlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'state', 'pincode')

class BookingAdmin(admin.ModelAdmin):
    pass
admin.site.register(Taxi, TaxiAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Booking, BookingAdmin)
# Register your models here.
