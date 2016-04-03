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
from runner import forms
from rest_framework import viewsets
from MySQLdb.cursors import SSDictCursor
from django.core.mail import send_mail


def send_email(user, pwd, recipient, subject, body):
    import smtplib

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    server.sendmail(FROM, TO, message)
    server.close()



def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def lower_keys(x):
    if isinstance(x, list):
       return [lower_keys(v) for v in x]
    elif isinstance(x, dict):
       return dict((k.lower(), lower_keys(v)) for k, v in x.iteritems())
    else:
       return x

# Create your views here.

def route_form(request):
    form = forms.RouteForm()

    return render(request, 'bus/routeform.html', {'form':form})

@api_view(['GET'],)
def get_stops(request):
    cursor = connection.cursor()
    sql = """select Stop.ID as id, Stop.NAME as name, Stop.CITY as city from Stop where Stop.ID != -1"""
    cursor.execute(sql)
    queryset = dictfetchall(cursor)
    #queryset = Stop.objects.raw(sql)
    result = StopSerializer(queryset, many=True)
    return Response(result.data)

@api_view(['POST', 'GET'],)
def get_routes(request):
    source = request.POST['source']
    dest = request.POST['dest']
    time = request.POST['time']
    now = '2016-02-10 17:00:00'
    sql = ROUTE_SEARCH_QUERY
    queryset = Route.objects.raw(sql, (source, dest, now, time, time) )
    result = RouteSerializer(queryset, many=True)
    return Response(result.data)

@api_view(['GET'])
def get_route_detail(request, id):
    cursor = connection.cursor()
    rid = id
    sql = ROUTE_DETAIL_QUERY
    cursor.execute(sql, (rid,))
    queryset = dictfetchall(cursor)
    #nqueryset = lower_keys(queryset)
    result = RouteDetailSerializer(queryset, many=True)
    return Response(result.data)

