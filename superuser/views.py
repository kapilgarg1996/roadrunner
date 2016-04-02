from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from MySQLdb.cursors import SSDictCursor
from django.core.mail import send_mail
from django.conf import settings
from django.core import signing
from .models import *
from datetime import datetime, timedelta
from .forms import *
import hashlib
from django.conf import settings
import importlib
from django.utils import timezone

setlist = settings.SUPERUSER_HANDLER.split('.')
modules = importlib.import_module('.'.join(setlist[:-1]))
data_handler = getattr(modules, setlist[-1])

setlist = settings.SUPERUSER_PHANDLER.split('.')
modules = importlib.import_module('.'.join(setlist[:-1]))
pass_handler = getattr(modules, setlist[-1])

def test_view(request):
    return HttpResponse("In superuser")

def signup(request):
    if request.method == 'POST':
        form = FormTemp(request.POST, request.FILES)
        only_update = False
        if form.is_valid():
            primary = form.cleaned_data[settings.SUPERUSER_PRIMARY]
            try:
                qdict = {}
                qdict[settings.SUPERUSER_PRIMARY] = primary
                user = UserTemp.objects.get(**qdict)
                if user.verified==True:
                    return HttpResponse("Account already exists")
                else:
                    only_update = True
            except:
                pass
                    
            email = form.cleaned_data[settings.SUPERUSER_MAIL]
            signer = hashlib.sha256()
            signer.update(primary)
            validation_key = signer.hexdigest()
            confirm_key = request.build_absolute_uri('/signup-confirm/')+'?key='+validation_key
            #send_mail('Confirm Your Mail', confirm_key, settings.EMAIL_HOST_USER, [email,])
            valid = Validation(key_data=validation_key, create_time=datetime.now(), expire_time=datetime.now()+timedelta(days=30))
            valid.save()
            formlist = form.fields.keys()
            fieldlist = []
            retlist = []
            for field in UserTemp._meta.get_fields():
                fieldlist.append(field.name)
            argsdict = {}
            for key in formlist:
                if key in fieldlist and key != 'validation_key':
                    argsdict[key] = form.cleaned_data[key]
                    retlist.append(argsdict[key])
            argsdict['validation_key'] = valid
            argsdict['verified'] = False
            if only_update:
                user.validation_key = valid
                user.save()
                return HttpResponse('Validation key updated')
            else:
                usertemp = UserTemp(**argsdict)
                usertemp.save()
                return HttpResponse(confirm_key)
        else:
            return HttpResponse('Invalid Data')
    else:
        return HttpResponse('What are you doing here ? Tresspass')


def password_reset(request):
    if request.method == 'POST':
        form = PRForm(request.POST)
        if form.is_valid():
            fields = settings.SUPERUSER_PRFIELDS
            args = {}
            for field in fields:
                args[field] = form.cleaned_data[field]

            args['verified'] = True
            try:
                user = UserTemp.objects.get(**args)
                
                email = form.cleaned_data[settings.SUPERUSER_MAIL]
                signer = hashlib.sha256()
                signer.update(str(timezone.now()))
                validation_key = signer.hexdigest()
                confirm_key = request.build_absolute_uri('/password-confirm/')+'?key='+validation_key
                #send_mail('Confirm Your Mail', confirm_key, settings.EMAIL_HOST_USER, [email,])

                valid = Validation(key_data=validation_key, create_time=datetime.now(), expire_time=datetime.now()+timedelta(days=30))
                valid.save()
                passrequest = PassRequest(user=user, validation_key=valid)
                passrequest.save()
                return HttpResponse(confirm_key)
            except:
                return HttpResponse("Wrong Credentials")

def login(request):
    if request.method=='POST':
        form = LFormTemp(request.POST)
        if form.is_valid():
            fields = settings.SUPERUSER_LOGLIST
            args = {}
            for field in fields:
                args[field] = form.cleaned_data[field]

            args['verified'] = True
            try:
                user = UserTemp.objects.get(**args)
                return HttpResponse("Logged in")
            except :
                return HttpResponse("Wrong Credentials")
        else:
            return HttpResponse("Oops")
    else:
        return HttpResponse("TressPass")
    


def confirm_signup(request):
    if request.method=='GET':
        try:
            key = request.GET['key']
        except:
            key = False
        if(key):
            try:
                valid_key = Validation.objects.get(key_data=key)
            except:
                return HttpResponse("Wrong Confirmation Key")
            nowtime = timezone.make_aware(datetime.now(), timezone.get_default_timezone())
            if(valid_key and nowtime<valid_key.expire_time):
                user = UserTemp.objects.get(validation_key = valid_key)
                user.verified = True
                user.save()
                data_handler(request, user.to_dict())
                return HttpResponse("User registered")
            else:
                return HttpResponse("Key has expired. Create a new account")
        else:
            return HttpResponse("Corrupted url")
    else:
        return HttpResponse("Tresspass")


def confirm_password(request):
    if request.method=='GET':
        try:
            key = request.GET['key']
        except:
            return HttpResponse("Corrupted Url")

        try:
            valid_key = Validation.objects.get(key_data=key)
        except:
            return HttpResponse("Wrong Conformation key")
        nowtime = timezone.now()
        if(nowtime<valid_key.expire_time):
            req = PassRequest.objects.get(validation_key=valid_key)
            req.request_verified = True
            req.save()
            form = PassForm(request.POST or None, initial = {'key_field':key})
            return render(request, settings.SUPERUSER_FORMTEMPLATE, {'form':form})
        else:
            return HttpResponse("Key has expired")
    elif request.method=='POST':
        form = PassForm(request.POST)
        if form.is_valid():
            key = form.cleaned_data['key_field']
            npass = form.cleaned_data['new_pass']
            rnpass = form.cleaned_data['repeat_pass']
            try:
                valid_key = Validation.objects.get(key_data=key)
            except:
                return HttpResponse("valid not found")
            try:
                pass_req = PassRequest.objects.get(validation_key=valid_key)
            except:
                return HttpResponse("Pass Request not found")
            user = pass_req.user
            if pass_req.request_verified==True and pass_req.pending==True:
                pass_req.pending = False
                pass_req.save()
                setattr(user, settings.SUPERUSER_PASSFIELD, npass)
                user.save()
                pass_handler(uid=user.id, password=npass)
                return HttpResponse("Password Changed")
            else:
                return HttpResponse("Invalid Request")
        else:
            return HttpResponse("Invalid Data")
    else:
        return HttpResponse("Tresspass")


            
