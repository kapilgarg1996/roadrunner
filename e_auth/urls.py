from django.conf.urls import url
from django.conf.urls import include
from . import views

urlpatterns = [
        url(r'^generate-form/', views.testform, name='test'),
        url(r'authorize-form/', views.testanother, name='test2'),
        url(r'^generate_token/', views.generate_token, name='generate_token'),
        url(r'^authorize/', views.authorize, name='authorize'),
]
