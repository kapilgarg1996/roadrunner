from django.conf.urls import url
from django.conf.urls import include
from . import views
import superuser
urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^request/stops/', views.send_stops, name='send_stops'),
        url(r'^test/', views.test, name='test'),
        url(r'signup/', include('superuser.urls')),
        url(r'^signup-form/', views.user_signup, name='signup'),
        url(r'^login/', views.login_form, name='login'),
        url(r'^stops/', views.get_stops, name='get_stops'),
        url(r'^routes/', views.get_routes, name='get_routes'),
        url(r'^route-search/', views.route_form, name='route_form'),
        url(r'^get-route/(?P<id>[0-9][0-9]*)', views.get_route_detail, name='route_detail'),
        url(r'get-user/(?P<id>[0-9][0-9]*)', views.get_user_detail, name='user_detail'),
]
