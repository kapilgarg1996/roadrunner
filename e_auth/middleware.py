import urllib, urllib2, json
from django.http import HttpResponse
from e_auth.models import *
from django.utils import timezone

def protector(func):
    def decorator(request, *args, **kwargs):
        app_name = request.resolver_match.app_name
        from django.conf import settings
        allowed_apps = settings.EAUTH_ALLOWEDAPPS
        if app_name in allowed_apps:
            return func(request, *args, **kwargs)

        token = request.GET.get('token') or request.POST.get('token')
        response = HttpResponse()
        if token:
            try:
                auth = Authorize.objects.get(auth_token=token)
            
                if(timezone.now() < auth.expire_time):
                    return func(request, *args, **kwargs)
                else:
                    retdict = {}
                    retdict['status'] = 400
                    retdict['data'] = "Token Has Expired"
                    retdict['detail'] = "Invalid Token"
                    response.status_code = 400
                    serialdata = json.dumps(retdict)
                    response.content = serialdata
                    return response
            except:
                    retdict = {}
                    retdict['status'] = 400
                    retdict['data'] = "User Not Authorized"
                    retdict['detail'] = "Invalid Token"
                    response.status_code = 400
                    serialdata = json.dumps(retdict)
                    response.content = serialdata
                    return response

        else:
            retdict = {}
            retdict['status'] = 404
            retdict['data'] = "Access Token Is Required"
            retdict['detail'] = "Unverified Request to restricted url"
            response.status_code = 404
            serialdata = json.dumps(retdict)
            response.content = serialdata
            return response

    return decorator
