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

def test_view(request):
    return HttpResponse("In superuser")

def signup(request):
    if request.method == 'POST':
        form = FormTemp(request.POST, request.FILES)
        if form.is_valid():
            primary = form.cleaned_data[settings.SUPERUSER_PRIMARY]
            email = form.cleaned_data[settings.SUPERUSER_MAIL]
            signer = hashlib.sha256()
            signer.update(primary)
            validation_key = signer.hexdigest()
            confirm_key = request.build_absolute_uri('/signup-confirm/')+'?key='+validation_key
            send_mail('Confirm Your Mail', confirm_key, settings.EMAIL_HOST_USER, [email,])
            valid = Validation(key_data=validation_key, create_time=datetime.now(), expire_time=datetime.now()+timedelta(days=30))
            valid.save()
            formlist = form.fields.keys()
            fieldlist = []
            for field in UserTemp._meta.get_fields():
                fieldlist.append(field.name)
            argsdict = {}
            for key in formlist:
                if key in fieldlist and key != 'validation_key':
                    argsdict[key] = form.cleaned_data[key]
            argsdict['validation_key'] = valid
            argsdict['verified'] = False
            usertemp = UserTemp(**argsdict)
            usertemp.save()
            return HttpResponse('Temp created')
        else:
            return HttpResponse('Invalid Data')
    else:
        return HttpResponse('What are you doing here ? Tresspass')

def signup_form(request):
    pass

def password_reset(request):
    pass

def login(request):
    pass

def login_form(reuqest):
    pass

def confirm_signup(request):
    if request.method=='GET':
        key = request.GET['key']
        if(key):
            valid_key = Validation.objects.get(key_data=key)
            nowtime = timezone.make_aware(datetime.now(), timezone.get_default_timezone())
            if(valid_key and nowtime<valid_key.expire_time):
                data_handler(request, UserTemp.objects.get(validation_key=valid_key.key).to_dict())
                return HttpResponse("User registered")
            else:
                return HttpResponse("Key has expired. Create a new account")
        else:
            return HttpResponse("Corrupted url")
    else:
        return HttpResponse("Tresspass")


def confirm_password(reuqest):
    pass
