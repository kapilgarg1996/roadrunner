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
    times=[]
    i=0
    for source in stops:
        for dest in stops:
            if source != dest and stops.index(source) < stops.index(dest):
                route = Route(source=source, dest=dest, start_time=stime, bus=bus, driver=driver, conductor=conductor)

                thread = threading.Thread(name='save', target=save, args=[route])
                thread.start()
                thread.join(5)
                if i==0:
                    times.append(route.journey_time)
        try:        
            stime = times[i] + timedelta(minutes=30)
        except:
            pass
        i+= 1

def route_adder(request):
    stopids = [4, 3, 5, 6]
    stime = datetime(2016, 4, 20, 6, 0, 0)
    driver = Employee.objects.get(id=3)
    conductor = Employee.objects.get(id=4)
    bus = Bus.objects.get(id=2)
    stops=[]
    for stopid in stopids:
        stop = Stop.objects.get(id=stopid)
        stops.append(stop)

    route_saver(stops, stime, driver, conductor, bus)

    return HttpResponse("Done")

