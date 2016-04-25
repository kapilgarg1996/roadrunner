from django.conf.urls import url
from django.conf.urls import include
from . import views

urlpatterns = [
        url(r'^paynow/', views.paynow, name='paynow'),
        url(r'^paylater/', views.paylater, name='paylater'),
        url(r'^addmoney/', views.addmoney, name='addmoney')
]

