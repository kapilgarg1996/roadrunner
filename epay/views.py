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

@api_view(['POST'])
def paynow(request):
    userid = request.POST['user']
    user = User.objects.get(id=int(userid))
    amount = int(request.POST['amount'])
    wallet = user.wallet


    ticketdata = {}
    bookingdata = {}
    if(request.POST['rtype']=='Taxi'):
        bookingdata['user'] = userid
        bookingdata['taxi'] = int(request.POST['taxi'])
        bookingdata['journey_time'] = datetime.strptime(request.POST['journey_time'], '%Y-%m-%d %H:%M:%S')
        bookingdata['source'] = request.POST['source']
        bookingdata['dest'] = request.POST['dest']
        bookingdata['payment_status'] = 'Successful'

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

        user.wallet = wallet-amount
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
        signer = hashlib.sha256()
        signer.update(str(timezone.now()))
        payment.token = signer.hexdigest()
        payment.status = True
        payment.save()
        data = {'status' : 'Payment Successful', 'token' : payment.token}
        sdata = PaymentSerializer(data)
        return Response(sdata.data)


@api_view(['POST'])
def paylater(request):
    pass

@api_view(['POST'])
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
