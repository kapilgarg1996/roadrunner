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
def increment(value, factor):
    return value + factor
def route_saver(stops, stime, driver, conductor, bus):
    start_time = stime
    times=[stime]
    routes = []
    for i in range(0, len(stops)-1):
        source = stops[i] ;
        dest = stops[i+1] ;
        route = Route(source=source, dest=dest, start_time=start_time, bus=bus, driver=driver, conductor=conductor)
        route.save()
        if (route.journey_time - start_time).total_seconds()< 10800:
            start_time = route.journey_time + timedelta(minutes=30)
        elif (route.journey_time - start_time).total_seconds()< 21600:
            start_time = route.journey_time + timedelta(minutes=60)
        elif (route.journey_time - start_time).total_seconds()< 43200:
            start_time = route.journey_time + timedelta(minutes=90)
        else:
            start_time = route.journey_time + timedelta(minutes=120)
        routes.append(route)

    for i in range(0, len(routes)-1):
        for j in range(i+1, len(routes)):
            t_fair = 0
            if(j==i+1):
                t_fair = routes[i].fair
            source = routes[i].source
            dest = routes[j].dest
            start = routes[i].start_time
            end = routes[j].journey_time
            t_fair += routes[j].fair
            route = Route(source=source, dest=dest, start_time=start, bus=bus, driver=driver, conductor=conductor, journey_time = end, fair=t_fair)
            route.save()

    return routes[len(routes)-1].journey_time

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
