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
# Create your views here.
def route_sel(request):
    pass

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

    return render(request, 'runner/signup.html', {'form':form})

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



def user_saver(request, userdata):
    user = User(**userdata)
    user.save()

