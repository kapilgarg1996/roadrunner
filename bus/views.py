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


# Create your views here.

def route_form(request):
    form = forms.RouteForm()
    return render(request, 'bus/routeform.html', {'form':form})

@api_view(['GET'],)
def get_stops(request):
    sql = """select * from bus_stop where bus_stop.id != -1"""
    queryset = Stop.objects.raw(sql)
    result = StopSerializer(queryset, many=True)
    return Response(result.data)

@api_view(['POST', 'GET'],)
def get_routes(request):
    source = request.POST['source']
    dest = request.POST['dest']
    time = request.POST['time']
    now = str(timezone.now())
    sql = ROUTE_SEARCH_QUERY
    queryset = Route.objects.raw(sql, (source, dest, now, time, time) )
    result = RouteSerializer(queryset, many=True)
    return Response(result.data)

@api_view(['GET'])
def get_route_detail(request, id):
    rid = id
    sql = ROUTE_DETAIL_QUERY
    queryset = Route.objects.raw(sql, (rid))
    result = RouteDetailSerializer(queryset, many=True)
    return Response(result.data)

