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
from e_auth.middleware import protector

# Create your views here.


@api_view(['GET', 'POST'],)
@protector
def get_stops(request):
    sql = """select * from bus_stop where bus_stop.id != -1"""
    queryset = Stop.objects.raw(sql)
    result = StopSerializer(queryset, many=True)
    return Response(result.data)

@api_view(['POST', 'GET'],)
@protector
def get_routes(request):
    source = request.POST['source']
    dest = request.POST['dest']
    time = request.POST['time']

    now = str(timezone.now())
    sql = ROUTE_SEARCH_QUERY
    queryset = Route.objects.raw(sql, (source, dest, now, time, time) )
    result = RouteSerializer(queryset, many=True)
    return Response(result.data)

@api_view(['GET', 'POST'])
@protector
def get_route_detail(request, id):
    rid = id
    sql = ROUTE_DETAIL_QUERY
    queryset = Route.objects.raw(sql, (rid,))
    result = RouteDetailSerializer(queryset, many=True)
    return Response(result.data)



@api_view(['POST'])
@protector
def book_ticket(request):
    try:
        uid = request.POST['user']
        rid = request.POST['route']
        payment = request.POST['payment_status']
        seats = request.POST['seats']
        seats_config = request.POST['seats_config']
        user = User.objects.get(id=uid)
        route = Route.objects.get(id=rid)
        book_time = timezone.now()
        price = route.fair*int(seats)
        status = check_seats(int(rid), int(seats), seats_config )
        if status==True:
            ticket = Ticket(user=user, route=route, seats=int(seats), price=price, book_time = book_time, seats_config=seats_config, payment_status=payment)
            ticket.save()
            serial_ticket = TicketSerializer(ticket)
            return Response(serial_ticket.data)
        else:
            data = {}
            data['detail'] = "Seats have been occupied. Choose other seat"
            response = Response()
            response.data = data
            return response
    except:
        response = Response(status=405)
        response.data = "Problem Encountered"
        return response

def check_seats(rid, numseats, seats_config):
    route = Route.objects.get(id=rid)
    for i in range(0, len(route.seats_config)):
        if seats_config[i]=='0' and route.seats_config[i]=='0':
            return False

    seats = ''
    for i in range(0, len(route.seats_config)):
        if route.seats_config[i]=='1' and seats_config[i]=='0':
            seats += '0'
        else:
            seats += route.seats_config[i]
    
    route.seats_avail -= numseats
    route.seats_config = seats
    route.save()
    
    return True
