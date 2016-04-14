from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import MySQLdb as mysql
from django.db import connection
from bus.queries import *
import json
from bus.serializers import *
from bus.models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from bus import forms
from rest_framework import viewsets
from MySQLdb.cursors import SSDictCursor
from django.core.mail import send_mail
from django.utils import timezone
from time import sleep
from datetime import datetime
import threading

def save(route):
    route.save()
def route_saver(stops, stime, driver, conductor, bus):
    stime = stime - timedelta(minutes=30)
    times=[stime]
    i=0
    for source in stops:
        try:
            stime = times[i] + timedelta(minutes=30)
        except:
            pass
        for dest in stops:
            if source != dest and stops.index(source) < stops.index(dest):
                route = Route(source=source, dest=dest, start_time=stime, bus=bus, driver=driver, conductor=conductor)

                #thread = threading.Thread(name='save', target=save, args=[route])
                #thread.start()
                #thread.join(5)
                route.save()
                if i==0:
                    times.append(route.journey_time)

        i+= 1

    return route.journey_time

def route_adder(request):
    stopids = []
    for key in range(len(request.POST.keys())):
        try:
            stopids.append(int(request.POST.get('stop'+str(key))))
        except:
            pass
    stime = datetime.strptime(request.POST['time'], '%Y-%m-%d %H:%M:%S')
    driver = Employee.objects.get(id=int(request.POST['driver']))
    conductor = Employee.objects.get(id=int(request.POST['conductor']))
    bus = Bus.objects.get(id=int(request.POST['bus']))
    stops=[]
    for stopid in stopids:
        stop = Stop.objects.get(id=stopid)
        stops.append(stop)

    last_time = route_saver(stops, stime, driver, conductor, bus)
    new_stops = []
    for stop in reversed(stops):
        new_stops.append(stop)

    new_time = datetime(last_time.year, last_time.month, last_time.day, last_time.hour+1, 0, 0)
    new_time = new_time + timedelta(hours=12)
    if (last_time - stime).total_seconds()< 43200:
        route_saver(new_stops, new_time, driver, conductor, bus)
    else:
        route_saver(new_stops, new_time+timedelta(hours=12), driver, conductor, bus)

    return HttpResponseRedirect('/admin/bus/route/')
