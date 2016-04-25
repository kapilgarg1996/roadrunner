from django import forms
from django.contrib.admin import widgets  
from django.forms import ModelForm
from runner.models import User
from bus.models import *
from taxi.models import *

def_ticket = '0'*56

class LoginForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    password = forms.CharField(label='Password', max_length=20, widget=forms.PasswordInput())
    
    #def clean(self):
    #    first_pass = self.cleaned_data['password']
    #    rep_pass = self.cleaned_data['repeat_password']
    #    if first_pass and rep_pass:
    #        if first_pass != rep_pass:
    #            raise forms.ValidationError('Passwords must match')

class Password(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)
    email = forms.EmailField(label='Your mail', max_length=100)

class RouteAddForm(forms.Form):
    stop1 = forms.ModelChoiceField(queryset=Stop.objects.all(), to_field_name="id")
    stop2 = forms.ModelChoiceField(queryset=Stop.objects.all(), to_field_name="id")
    stop3 = forms.ModelChoiceField(queryset=Stop.objects.all(), to_field_name="id")
    stop4 = forms.ModelChoiceField(queryset=Stop.objects.all(), to_field_name="id")
    stop5 = forms.ModelChoiceField(queryset=Stop.objects.all(), to_field_name="id")
    time = forms.DateTimeField()
    bus = forms.ModelChoiceField(queryset=Bus.objects.filter(available=True), to_field_name='id')
    driver = forms.ModelChoiceField(queryset=Employee.objects.filter(post='DRIVER'), to_field_name='id')
    conductor = forms.ModelChoiceField(queryset=Employee.objects.filter(post='Conductor'), to_field_name='id')

class StopsForm(forms.Form):
    token = forms.CharField(label="token", max_length=200 )

class RouteForm(forms.Form):
    source = forms.ModelChoiceField(queryset=Stop.objects.all(), to_field_name="name")
    dest = forms.ModelChoiceField(queryset=Stop.objects.all(), to_field_name="name")
    time = forms.DateTimeField()
    token = forms.CharField(label='token', max_length=200)

class BusBookForm(forms.ModelForm):
    rtype = forms.CharField()
    token = forms.CharField(max_length=200)
    payment_status = forms.CharField()
    class Meta:
        model = Ticket
        fields = ('user', 'route', 'seats', 'seats_config')

class UserSignupForm(ModelForm):
    class Meta:
        model = User
        exclude = ('id',)

class AuthForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField()

class TokenForm(forms.Form):
    token = forms.CharField(max_length=200)

class PassForm(forms.Form):
    key_field = forms.CharField(max_length=200)
    new_pass = forms.CharField(max_length=100)
    repeat_pass = forms.CharField(max_length=100)

class BookingForm(ModelForm):
    rtype = forms.CharField()
    token = forms.CharField(max_length=200)
    class Meta:
        model = Booking
        fields = ('user', 'taxi', 'journey_time', 'source', 'dest')

