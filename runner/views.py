from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import MySQLdb as mysql
from django.db import connection
from runner.queries import *
import json
#from runner.serializers import StopSerializer, RouteSerializer, RouteDetailSerializer
from runner.serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from runner import forms
from rest_framework import viewsets
from MySQLdb.cursors import SSDictCursor
from django.core.mail import send_mail
from runner.models import *

#from django.core.mail import send_mail


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def index(request):
    return HttpResponse("Hello kapil")



@api_view(['GET'])
def get_user_detail(request, id):
    cursor = connection.cursor()
    uid = id
    sql = USER_DETAIL_QUERY
    cursor.execute(sql, (uid,))
    queryset = dictfetchall(cursor)
    result = UserDetailSerializer(queryset, many=True)
    return Response(result.data)

@api_view(['POST', 'GET'])
def get_user_by_name(request):
    if request.method=="GET":
        uname = request.GET['username']
    elif request.method == "POST":
        uname = request.POST['username']
    try:
        user = User.objects.get(name=uname)
        serial_user = UserSerializer(user)
        return Response(serial_user.data)
    except:
        return Response("NO_DATA", status=404)

@api_view(['GET'])
def get_user(request, id):
    uid = id
    try:
        user = User.objects.get(id=uid)
        serial_user = UserSerializer(user)
        return Response(serial_user.data)
    except:
        return Response("NO_DATA", status=404)

def user_saver(request, userdata):
    user = User(**userdata)
    user.save()

def pass_handler(uid='', password=''):
    user = User.objects.get(email=uid)
    user.password = password
    user.save()

# Forms for testing Roadrunner API

def login_form(request):
    form = forms.LoginForm()
    return render(request, 'runner/common.html', {'form':form, 'url':'/superuser/login/', 'button': 'Log In'})

def user_signup(request):
    form = forms.UserSignupForm()
    return render(request, 'runner/common.html', {'form': form, 'url':'/superuser/signup/', 'button':'Sign Up'})

def route_form(request):
    form = forms.RouteForm()
    return render(request, 'runner/common.html', {'form':form, 'url':'/bus/routes/', 'button':'Search Route'})

def stops_form(request):
    form = forms.StopsForm()
    return render(request, 'runner/common.html', {'form':form, 'url':'/bus/stops/', 'button':'Get Stops'})

def change_password(request):
    form = forms.Password()
    return render(request, 'runner/common.html', {'form':form, 'url':'/superuser/password-reset/', 'button':'Generate Password Request'})

def taxi_form(request):
    form = forms.BookingForm()
    return render(request, 'runner/common.html', {'form':form, 'url':'/taxi/book-taxi/', 'button':'Book Taxi'})

def bus_form(request):
    form = forms.BusBookForm()
    return render(request, 'runner/common.html', {'form':form, 'url':'/bus/book-ticket/', 'button':'Book Bus Ticket'})

def generate_form(request):
    form = forms.AuthForm()
    return render(request, 'runner/common.html', {'form':form, 'url':'/e-auth/generate_token/', 'button':'Generate Token'})

def authorize_form(request):
    form = forms.TokenForm()
    return render(request, 'runner/common.html', {'form':form, 'url':'/e-auth/authorize/', 'button':'Authorize Token'})

def enter_pass(request):
    form = forms.PassForm()
    return render(request, 'runner/common.html', {'form':form, 'url':'/superuser/password-confirm/', 'button':'Change Password'})

