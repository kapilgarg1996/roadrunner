"""roadrunner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from runner import views
from rest_framework import routers
import account

urlpatterns = [
    url(r'^epay/', include('epay.urls', namespace='epay', app_name='epay')),
    url(r'^bus/', include('bus.urls', namespace='bus', app_name='bus')),
    url(r'^taxi/', include('taxi.urls', namespace='taxi', app_name='taxi')),
    url(r'^superuser/', include('superuser.urls', namespace='superuser', app_name='superuser')),
    url(r'^e-auth/', include('e_auth.urls', namespace='e_auth', app_name='e_auth')),
    url(r'^runner/', include('runner.urls', namespace='e_auth', app_name='runner')),
    url(r'^admin/', admin.site.urls),
]
