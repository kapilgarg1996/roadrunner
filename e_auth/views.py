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
from e_auth.forms import * 
from e_auth.models import *
from e_auth.serializers import *
setlist = settings.EAUTH_USER.split('.')
UserApp = importlib.import_module('.'.join(setlist[:-1]))
User = getattr(UserApp, setlist[-1])


@api_view(['POST'])
def generate_token(request):
    response = Response(status=405)
    if request.method=='POST':
        response.status = 404
        fieldlist = settings.EAUTH_FIELDS
        argsdict = {}
        for field in fieldlist:
            argsdict[field] = request.POST.get(field)
        try:
            user = User.objects.get(**argsdict)
            response.status = 200
        except:
            response.status = 404
            return response
        
        signer = hashlib.sha256()
        signer.update(str(timezone.now()))
        validation_key = signer.hexdigest()
        
        try:
            auth = Authorize.objects.get(user=user)
        except:
            auth = Authorize()
            auth.user = user

        auth.auth_token = validation_key
        auth.create_time = timezone.now()
        auth.expire_time = timezone.now() + timedelta(days=30)
        auth.save()

        data = {'status':200, 'token':validation_key}
        sdata = TokenSerializer(data)
        response.data = sdata.data
        return response
    else:
        return response



@api_view(['POST'])
def authorize(request):
    pass

def testform(request):
    form = AuthForm()
    return render(request, 'e_auth/form.html', {'form':form})
