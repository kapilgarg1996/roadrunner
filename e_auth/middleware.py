import urllib, urllib2, json
from django.http import HttpResponse

class AuthorizeMiddleware(object):
    def process_view(self, request, request_view, view_args, view_kwargs):
        app_name = request.resolver_match.app_name
        from django.conf import settings
        allowed_apps = settings.EAUTH_ALLOWEDAPPS
        if app_name in allowed_apps:
            return None

        token = request.GET.get('token') or request.POST.get('token')
        response = HttpResponse()
        if token:
            url = request.build_absolute_uri("/e-auth/authorize/")
            mdict = {'token':token}
            udata = urllib.urlencode(mdict)
            req = urllib2.Request(url, udata)

            try:
                res = urllib2.urlopen(req)
                status = res.code
            except:
                retdict = {}
                retdict['status'] = 400
                retdict['data'] = "User Not Authorized"
                retdict['detail'] = "Not Authenticated"
                response.status_code = 400
                serialdata = json.dumps(retdict)
                response.content = serialdata
                return response
            if status==200:
                content = res.read()
                auth_status = json.loads(content)
                if auth_status['authorized']==True:
                    return None
                else:
                    retdict = {}
                    retdict['status'] = 400
                    retdict['data'] = "User Not Authorized"
                    retdict['detail'] = auth_status['authorized']
                    response.status_code = 400
                    serialdata = json.dumps(retdict)
                    response.content = serialdata
                    return response

            else:
                retdict = {}
                retdict['status'] = 400
                retdict['data'] = "User Not Authorized"
                retdict['detail'] = "Not Authenticated"
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
