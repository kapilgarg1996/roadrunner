from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.conf import settings
import importlib
import hashlib
import json
from django.utils import timezone
from datetime import datetime, timedelta
from epay.models import *
from epay.serializers import *
from runner.models import *
from bus.models import *
from taxi.models import *
import urllib, urllib2
from e_auth.middleware import protector

@api_view(['POST'])
@protector
def paynow(request):
    userid = request.POST['user']
    user = User.objects.get(id=int(userid))
    wallet = user.wallet
    usertoken = request.POST['token']
    ticketdata = {}
    bookingdata = {'token': usertoken}
    if(request.POST['rtype']=='Taxi'):
        bookingdata['user'] = userid
        bookingdata['taxi'] = int(request.POST['taxi'])
        bookingdata['journey_time'] = datetime.strptime(request.POST['journey_time'], '%Y-%m-%d %H:%M:%S')
        bookingdata['source'] = request.POST['source']
        bookingdata['dest'] = request.POST['dest']
        signer = hashlib.sha256()
        signer.update(str(timezone.now()))
        token = signer.hexdigest()
        bookingdata['payment_status'] = token

        source = Place.objects.get(id=request.POST['source'])
        dest = Place.objects.get(id=request.POST['dest'])
        datadict = gmaps(source=urllib.quote(source.get_location()), dest=urllib.quote(dest.get_location()))
        taxi = Taxi.objects.get(id=request.POST['taxi'])
        fair = taxi.fair_ratio*datadict['distance']
        fair = fair/1000

        if(fair > wallet):
            data = {'status': 'Wallet is short of money', 'token': 'NO_DATA'}
            sdata = PaymentSerializer(data)
            return Response(sdata.data)

        user.wallet = wallet-fair
        user.save()
        url = 'http://roadrunner.com/taxi/book-taxi/'
        data = urllib.urlencode(bookingdata)
        req = urllib2.Request(url, data)
        res = urllib2.urlopen(req)
        content = json.loads(res.read())
        bid = int(content['id'])
        payment = TaxiPayment()
        payment.user = user
        payment.booking = Booking.objects.get(id=bid)
        payment.time = timezone.now()
        payment.token = token
        payment.status = True
        payment.save()
        data = {'id': bid, 'status' : 'Payment Successful', 'token' : payment.token}
        sdata = PaymentSerializer(data)
        return Response(sdata.data)

    elif(request.POST['rtype']=='Bus'):
        bookingdata['user'] = userid
        bookingdata['route'] = int(request.POST['route'])
        bookingdata['seats'] = request.POST['seats']
        bookingdata['seats_config'] = request.POST['seats_config']
        signer = hashlib.sha256()
        signer.update(str(timezone.now()))
        token = signer.hexdigest()
        bookingdata['payment_status'] = token

        route = Route.objects.get(id=request.POST['route'])
        fair = route.fair*int(bookingdata['seats'])
        if(fair > wallet):
            data = {'status': 'Wallet is short of money', 'token': 'NO_DATA'}
            sdata = PaymentSerializer(data)
            return Response(sdata.data)

        user.wallet = wallet-fair
        user.save()
        url = 'http://roadrunner.com/bus/book-ticket/'
        data = urllib.urlencode(bookingdata)
        req = urllib2.Request(url, data)
        res = urllib2.urlopen(req)
        content = json.loads(res.read())
        tid = int(content['id'])
        payment = TaxiPayment()
        payment.user = user
        payment.ticket = Ticket.objects.get(id=tid)
        payment.time = timezone.now()
        payment.token = token
        payment.status = True
        payment.save()
        data = {'id':tid, 'status' : 'Payment Successful', 'token' : payment.token}
        sdata = PaymentSerializer(data)
        return Response(sdata.data)


@api_view(['POST'])
@protector
def paylater(request):
    userid = request.POST['user']
    user = User.objects.get(id=int(userid))
    wallet = user.wallet
    usertoken = request.POST['token']
    ticketdata = {}
    bookingdata = {'token':usertoken}
    if(request.POST['rtype']=='Taxi'):
        bookingdata['user'] = userid
        bookingdata['taxi'] = int(request.POST['taxi'])
        bookingdata['journey_time'] = datetime.strptime(request.POST['journey_time'], '%Y-%m-%d %H:%M:%S')
        bookingdata['source'] = request.POST['source']
        bookingdata['dest'] = request.POST['dest']
        signer = hashlib.sha256()
        signer.update(str(timezone.now()))
        token = signer.hexdigest()
        bookingdata['payment_status'] = token

        source = Place.objects.get(id=request.POST['source'])
        dest = Place.objects.get(id=request.POST['dest'])
        datadict = gmaps(source=urllib.quote(source.get_location()), dest=urllib.quote(dest.get_location()))
        taxi = Taxi.objects.get(id=request.POST['taxi'])
        fair = taxi.fair_ratio*datadict['distance']
        fair = fair/1000
        fair = fair/5
        if(fair > wallet):
            data = {'status': 'Wallet is short of money', 'token': 'NO_DATA'}
            sdata = PaymentSerializer(data)
            return Response(sdata.data)

        url = 'http://roadrunner.com/taxi/book-taxi/'
        data = urllib.urlencode(bookingdata)
        req = urllib2.Request(url, data)
        res = urllib2.urlopen(req)
        content = json.loads(res.read())
        bid = int(content['id'])
        payment = TaxiPayment()
        payment.user = user
        payment.booking = Booking.objects.get(id=bid)
        payment.time = timezone.now()
        payment.token = token
        payment.status = False
        payment.save()
        data = {'id':bid, 'status' : 'Later Payment Approved', 'token' : payment.token}
        sdata = PaymentSerializer(data)
        return Response(sdata.data)

    elif(request.POST['rtype']=='Bus'):
        bookingdata['user'] = userid
        bookingdata['route'] = int(request.POST['route'])
        bookingdata['seats'] = request.POST['seats']
        bookingdata['seats_config'] = request.POST['seats_config']
        signer = hashlib.sha256()
        signer.update(str(timezone.now()))
        token = signer.hexdigest()
        bookingdata['payment_status'] = token

        route = Route.objects.get(id=request.POST['route'])
        fair = route.fair*int(bookingdata['seats'])
        fair = route.fair/5
        if(fair > wallet):
            data = {'status': 'Wallet is short of money', 'token': 'NO_DATA'}
            sdata = PaymentSerializer(data)
            return Response(sdata.data)

        url = 'http://roadrunner.com/bus/book-ticket/'
        data = urllib.urlencode(bookingdata)
        req = urllib2.Request(url, data)
        res = urllib2.urlopen(req)
        content = json.loads(res.read())
        tid = int(content['id'])
        payment = TaxiPayment()
        payment.user = user
        payment.ticket = Ticket.objects.get(id=tid)
        payment.time = timezone.now()
        payment.token = token
        payment.status = True
        payment.save()
        data = {'id': tid, 'status' : 'Later Payment Approved', 'token' : payment.token}
        sdata = PaymentSerializer(data)
        return Response(sdata.data)

@api_view(['POST'])
@protector
def addmoney(request):
    pass

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
