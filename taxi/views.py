from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from taxi.serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from taxi.models import *
from runner.models import User
import urllib, urllib2
from datetime import timedelta, datetime
from django.utils import timezone
import json

@api_view(['GET'])
def get_taxis(request):
    taxis = Taxi.objects.filter(available=True)
    serial_taxi = TaxiSerializer(taxis, many=True)
    return Response(serial_taxi.data)

@api_view(['GET'])
def get_places(request):
    places = Place.objects.filter(available=True)
    serial_places = PlaceSerializer(places, many=True)
    return Response(serial_places.data)

@api_view(['GET'])
def taxi_detail(request):
    response = Response()
    response.status_code = 405
    tid = request.GET['id']
    if(tid):
        try:
            taxi = Taxi.objects.get(id=tid)
            serial_taxi = TaxiSerializer(taxi, many=True)
            response.status_code = 200
            response.data = serial_taxi.data
            return response
        except:
            response.data = "TAXI NOT FOUND"
            return response
    else:
        response.data = "Corrupted URL"
        return response


@api_view(['GET'])
def taxi_choice(request):
    choicedict = {}
    for key in request.GET.keys():
        choicedict[key] = request.GET[key]
    taxis = Taxi.objects.filter(**choicedict)
    serial_taxi = TaxiSerializer(taxis, many=True)
    return Response(serial_taxi.data)

@api_view(['POST'])
def book_taxi(request):
    #try:
        uid = request.POST['user']
        tid = request.POST['taxi']
        j_time = request.POST['journey_time']
        src = request.POST['source']
        dst = request.POST['dest']
        payment = request.POST['payment_status']
        user = User.objects.get(id=uid)
        driver = Driver.objects.filter(available=True)[0]
        taxi = Taxi.objects.get(id=tid)
        source = Place.objects.get(id=src)
        dest = Place.objects.get(id=dst)
        datadict = gmaps(source=urllib.quote(source.get_location()), dest=urllib.quote(dest.get_location()))
        fair = taxi.fair_ratio*datadict['distance']/1000
        j_etime = datetime.strptime(j_time, '%Y-%m-%d %H:%M:%S') + timedelta(seconds=datadict['time'])
    
        booking = Booking(user=user, taxi = taxi, driver=driver, source=source, dest=dest, journey_time=j_time, journey_endtime = j_etime, booking_time=timezone.now(), fair = fair, payment_status = payment)

        booking.save()
        serial_booking = BookingSerializer(booking)
        return Response(serial_booking.data)
    #except:
    #    response = Response(status=405)
    #    response.data = "Problem Encountered"
    #    return response
    


def gmaps(source='', dest=''):
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

