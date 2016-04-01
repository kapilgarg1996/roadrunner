from django.conf.urls import url
from django.conf.urls import include
from . import views

urlpatterns = [
        url(r'^signup/', views.signup, name='signup'),
        url(r'^signup-form/', views.signup_form, name='signup_form'),
        url(r'^login/', views.login, name='login'),
        url(r'^login-form/', views.login_form, name='login_form'),
        url(r'^password-reset/', views.password_reset, name='password_reset'),
        url(r'^signup-confirm/', views.confirm_signup, name='confirm_signup'),
        url(r'^confirm-password/', views.confirm_password, name='confirm_password'),
]

