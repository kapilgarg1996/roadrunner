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
def route_form(request):
    form = forms.RouteForm()
    return render(request, 'runner/routeform.html', {'form':form})

def stops_form(request):
    form = forms.StopsForm()
    return render(request, 'runner/stops.html', {'form':form})
def change_password(request):
    form = forms.Password()
    return render(request, 'runner/pass.html', {'form':form})


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def index(request):
    return HttpResponse("Hello kapil")

def send_stops(request):
    db = mysql.connect("localhost", "root", "kapilgarg", "roadrunner")
    cursor = db.cursor(SSDictCursor)
    sql = "select * from Stop"
    cursor.execute(sql)
    result = {}
    for i in range(0, 5):
        row = cursor.fetchone()
        ide = row['ID']
        del row['ID']
        x = int(ide)
        result[x] = row
    db.close()
    return HttpResponse(json.dumps(result))


def login_form(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            cursor = connection.cursor()
            sql = """
            select * from User where NAME = %s and PASSWORD = %s
            """
            cursor.execute(sql, (form.cleaned_data['username'], form.cleaned_data['password']))
            if cursor.rowcount == 1:
                return HttpResponse("Welcome")
            else:
                return HttpResponse("Cant login")
        else:
            return HttpResponse("Not a valid account")

    else:
        form = forms.LoginForm()

    return render(request, 'runner/login.html', {'form':form})

def test(request):
    return render(request, 'runner/test.html')

def user_signup(request):
    if request.method=='POST':
        form = forms.UserSignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            #send_email('kapilgarg1996@gmail.com', 'idlztwqtrnquuali', ['kapilgarg1996@gmail.com'], 'Test', 'Test Mail')
            send_mail('Subject here', 'Here is the message.', 'from@example.com',
                        ['kapilgarg1996@gmail.com'], fail_silently=False)
            return HttpResponse("Account Created")
            #form.save()
        else:
            return HttpResponse("Problem Occurred")
    else:
        form = forms.UserSignupForm()

    return render(request, 'runner/signup.html', {'form': form})


@api_view(['GET'],)
def get_user_detail(request, id):
    cursor = connection.cursor()
    uid = id
    sql = USER_DETAIL_QUERY
    cursor.execute(sql, (uid,))
    queryset = dictfetchall(cursor)
    result = UserDetailSerializer(queryset, many=True)
    return Response(result.data)


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

def taxi_form(request):
    form = forms.BookingForm()
    return render(request, 'runner/taxi.html', {'form':form})

def generate_form(request):
    form = forms.AuthForm()
    return render(request, 'runner/form.html', {'form':form})

def authorize_form(request):
    form = forms.TokenForm()
    return render(request, 'runner/anform.html', {'form':form})

def enter_pass(request):
    form = forms.PassForm()
    return render(request, 'runner/passform.html', {'form':form})

