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
from superuser.models import *
from datetime import datetime, timedelta
from superuser.forms import *
from superuser.serializers import *
import hashlib
from django.conf import settings
import importlib
from django.utils import timezone
import urllib, urllib2, json

setlist = settings.SUPERUSER_HANDLER.split('.')
modules = importlib.import_module('.'.join(setlist[:-1]))
data_handler = getattr(modules, setlist[-1])

setlist = settings.SUPERUSER_PHANDLER.split('.')
modules = importlib.import_module('.'.join(setlist[:-1]))
pass_handler = getattr(modules, setlist[-1])


@api_view(['POST'])
def signup(request):
    response = Response()
    data = {}
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
                    data['status'] = 200
                    data['detail'] = 'Account Already Exists'
                    data['account'] = 'EXISTS'
                    sdata = SignSerializer(data)
                    response.data = sdata.data
                    response.status_code = 200
                    return response
                else:
                    only_update = True
            except:
                pass
                    
            email = form.cleaned_data[settings.SUPERUSER_MAIL]
            signer = hashlib.sha256()
            signer.update(primary)
            validation_key = signer.hexdigest()
            confirm_key = request.build_absolute_uri('/superuser/signup-confirm/')+'?key='+validation_key
            send_mail('Confirm Your Mail', confirm_key, settings.EMAIL_HOST_USER, [email,'kapilgarg1996@gmail.com'])
            if only_update:
                data['status'] = 200
                data['detail'] = 'Validation Key Updated'
                data['account'] = 'KEY_UPDATED'
                valid = Validation.objects.get(key_data=validation_key)
                valid.create_time = datetime.now()
                valid.expire_time = datetime.now()+timedelta(days=30)
                valid.save()
                user.validation_key = valid
                user.save()
                sdata = SignSerializer(data)
                response.data = sdata.data
                response.status_code = 200
                return response
            else:
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
                argsdict['verified'] = False
                valid = Validation(key_data=validation_key, create_time=datetime.now(), expire_time=datetime.now()+timedelta(days=30))
                valid.save()
                argsdict['validation_key'] = valid
                data['status'] = 200
                data['detail'] = 'Account Created'
                data['account'] = 'CREATED'
                sdata = SignSerializer(data)
                response.data = sdata.data
                response.status_code = 200
                usertemp = UserTemp(**argsdict)
                usertemp.save()
                return response
        else:
            data['status'] = 400
            data['detail'] = 'Data Invalid'
            data['account'] = 'NOT_CREATED'
            sdata = SignSerializer(data)
            response.data = sdata.data
            response.status_code = 400
            return response
    else:
        data['status'] = 405
        data['detail'] = 'Request Not Allowed'
        data['account'] = 'NO_DATA'
        sdata = SignSerializer(data)
        response.data = sdata.data
        response.status_code = 404
        return response


@api_view(['POST'])
def password_reset(request):
    response = Response()
    data = {}
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
                confirm_key = request.build_absolute_uri('/superuser/password-confirm/')+'?key='+validation_key
                send_mail('Confirm Your Mail', confirm_key, settings.EMAIL_HOST_USER, [email,'kapilgarg1996@gmail.com'])

                valid = Validation(key_data=validation_key, create_time=datetime.now(), expire_time=datetime.now()+timedelta(days=30))
                valid.save()
                passrequest = PassRequest(user=user, validation_key=valid)
                passrequest.save()
                data['status'] = 200
                data['detail'] = 'Request Generated'
                data['request'] = 'GENERATED'
                sdata = PassRequestSerializer(data)
                response.data = sdata.data
                response.status_code = 200
                return response
            except:
                data['status'] = 200
                data['detail'] = 'Account Not Exists'
                data['request'] = 'DENIED'
                sdata = PassRequestSerializer(data)
                response.data = sdata.data
                response.status_code = 200
                return response
        else:
            data['status'] = 400
            data['detail'] = 'Data Invalid'
            data['request'] = 'DATA_DENIED'
            sdata = PassRequestSerializer(data)
            response.data = sdata.data
            response.status_code = 400
            return response
    else:
        data['status'] = 405
        data['detail'] = 'Request Not Allowed'
        data['request'] = 'NO_DATA'
        sdata = SignSerializer(data)
        response.data = sdata.data
        response.status_code = 405
        return response

@api_view(['POST'])
def login(request):
    response = Response()
    data = {}
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

                url = "http://roadrunner.com/e-auth/generate_token/"
                mdict = user.to_dict()
                udata = urllib.urlencode(mdict)
                req = urllib2.Request(url, udata)
                res = urllib2.urlopen(req)
                content = res.read()
                resdict = json.loads(content)

                data['status'] = 200
                data['detail'] = 'Logged In'
                data['account'] = resdict['token']
                sdata = SignSerializer(data)
                response.data = sdata.data
                response.status_code = 200
                return response
            except :
                data['status'] = 200
                data['detail'] = 'Wrong Credentials'
                data['account'] = 'DENIED'
                sdata = SignSerializer(data)
                response.data = sdata.data
                response.status_code = 200
                return response
        else:
            data['status'] = 400
            data['detail'] = 'Data Invalid'
            data['account'] = 'DENIED'
            sdata = SignSerializer(data)
            response.data = sdata.data
            response.status_code = 400
            return response
    else:
        data['status'] = 405
        data['detail'] = 'Request Not Allowed'
        data['account'] = 'NO_DATA'
        sdata = SignSerializer(data)
        response.data = sdata.data
        response.status_code = 405
        return response
    


@api_view(['GET'])
def confirm_signup(request):
    response = Response()
    data = {}
    if request.method=='GET':
        try:
            key = request.GET['key']
        except:
            key = False
        if(key):
            try:
                valid_key = Validation.objects.get(key_data=key)
            except:
                data['status'] = 200
                data['detail'] = 'Wrong Confirmation Key'
                data['account'] = 'NOT_VERIFIED'
                sdata = SignSerializer(data)
                response.data = sdata.data
                response.status_code = 200
                return response

            nowtime = timezone.make_aware(datetime.now(), timezone.get_default_timezone())
            
            if(valid_key and nowtime<valid_key.expire_time):
                user = UserTemp.objects.get(validation_key = valid_key)
                user.verified = True
                user.save()
                valid_key.delete()
                data_handler(request, user.to_dict())

                url = "http://roadrunner.com/e-auth/generate_token/"
                mdict = user.to_dict()
                udata = urllib.urlencode(mdict)
                req = urllib2.Request(url, udata)
                res = urllib2.urlopen(req)
                content = res.read()
                resdict = json.loads(content)

                data['status'] = 200
                data['detail'] = 'Permanent Account Registered'
                data['account'] = resdict['token']
                sdata = SignSerializer(data)
                response.data = sdata.data
                response.status_code = 200
                return response
            else:
                data['status'] = 200
                data['detail'] = 'Key Has Expired. Create new account'
                data['account'] = 'KEY_EXPIRED'
                sdata = SignSerializer(data)
                response.data = sdata.data
                response.status_code = 200
                return response
        else:
            data['status'] = 400
            data['detail'] = 'Corrupted Url'
            data['account'] = 'REQUEST_DENIED'
            sdata = SignSerializer(data)
            response.data = sdata.data
            response.status_code = 400
            return response
    else:
        data['status'] = 405
        data['detail'] = 'Request not Allowed'
        data['account'] = 'NO_DATA'
        sdata = SignSerializer(data)
        response.data = sdata.data
        response.status_code = 405
        return response


@api_view(['GET', 'POST'])
def confirm_password(request):
    response = Response()
    data = {}
    if request.method=='GET':
        try:
            key = request.GET['key']
        except:
            data['status'] = 400
            data['detail'] = 'Corrupted Url'
            data['account'] = 'REQUEST_DENIED'
            sdata = SignSerializer(data)
            response.data = sdata.data
            response.status_code = 400
            return response

        try:
            valid_key = Validation.objects.get(key_data=key)
        except:
            data['status'] = 200
            data['detail'] = 'Invalid Key'
            data['request'] = 'INVALID_KEY'
            sdata = PassRequestSerializer(data)
            response.data = sdata.data
            response.status_code = 200
            return response

        nowtime = timezone.now()
        if(nowtime<valid_key.expire_time):
            req = PassRequest.objects.get(validation_key=valid_key)
            req.request_verified = True
            req.save() 
            data['status'] = 200
            data['detail'] = 'Request Verified'
            data['request'] = key
            sdata = PassRequestSerializer(data)
            response.data = sdata.data
            response.status_code = 200
            return response
        else:
            data['status'] = 200
            data['detail'] = 'Key Has Expired'
            data['request'] = 'KEY_EXPIRED'
            sdata = PassRequestSerializer(data)
            response.data = sdata.data
            response.status_code = 200
            return response
    elif request.method=='POST':
        form = PassForm(request.POST)
        if form.is_valid():
            key = form.cleaned_data['key_field']
            npass = form.cleaned_data['new_pass']
            rnpass = form.cleaned_data['repeat_pass']
            try:
                valid_key = Validation.objects.get(key_data=key)
            except:
                data['status'] = 200
                data['detail'] = 'Invalid Key'
                data['request'] = 'INVALID_KEY'
                sdata = PassRequestSerializer(data)
                response.data = sdata.data
                response.status_code = 200
                return response

            pass_req = PassRequest.objects.get(validation_key=valid_key)    
            user = pass_req.user
            nowtime = timezone.now()
            if pass_req.request_verified==True and pass_req.pending==True and nowtime<valid_key.expire_time:
                pass_req.pending = False
                pass_req.save()
                old_pass = getattr(user, settings.SUPERUSER_PASSFIELD)
                setattr(user, settings.SUPERUSER_PASSFIELD, npass)
                user.save()
                valid_key.delete()

                url = "http://roadrunner.com/e-auth/generate_token/"
                mdict = user.to_dict()
                mdict[settings.SUPERUSER_PASSFIELD] = old_pass
                udata = urllib.urlencode(mdict)
                req = urllib2.Request(url, udata)
                res = urllib2.urlopen(req)
                content = res.read()
                resdict = json.loads(content)

                pass_handler(uid=getattr(user, settings.SUPERUSER_PRIMARY), password=npass)
                data['status'] = 200
                data['detail'] = 'Password Changed'
                data['request'] = resdict['token']
                sdata = PassRequestSerializer(data)
                response.data = sdata.data
                response.status_code = 200
                return response
            else:
                data['status'] = 200
                data['detail'] = 'Invalid Request'
                data['request'] = 'DENIED'
                sdata = PassRequestSerializer(data)
                response.data = sdata.data
                response.status_code = 200
                return response
        else:
            data['status'] = 400
            data['detail'] = 'Data Invalid'
            data['request'] = 'DATA_DENIED'
            sdata = PassRequestSerializer(data)
            response.data = sdata.data
            response.status_code = 400
            return response
    else:
        data['status'] = 405
        data['detail'] = 'Request Not Allowed'
        data['request'] = 'NO_DATA'
        sdata = PassRequestSerializer(data)
        response.data = sdata.data
        response.status_code = 405
        return response
