from django.conf.urls import url
from django.conf.urls import include
from . import views

urlpatterns = [
        url(r'^signup/', views.signup, name='signup'),
        url(r'^login/', views.login, name='login'),
        url(r'^password-reset/', views.password_reset, name='password_reset'),
        url(r'^password-new/', views.enter_pass, name='new_pass'),
        url(r'^signup-confirm/', views.confirm_signup, name='confirm_signup'),
        url(r'^password-confirm/', views.confirm_password, name='confirm_password'),
]

