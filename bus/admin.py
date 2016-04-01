from django.contrib import admin
from .models import *
class BusAdmin(admin.ModelAdmin):
    list_filter = ('available', 'ac', 'seater')
    list_display = ('id', 'number', 'ac', 'seater', 'total_seats', 'available')

class EmployeeAdmin(admin.ModelAdmin):
    list_filter = ('post',)
    list_display = ('id', 'name', 'shift', 'post', 'account')


class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'route', 'seats', 'price', 'book_time')

class RouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'dest', 'driver', 'conductor', 'bus', 'start_time', 'seats_avail')

class StopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city')

admin.site.register(Bus, BusAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Stop, StopAdmin)

# Register your models here.
