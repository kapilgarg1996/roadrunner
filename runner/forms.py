from django import forms
from django.contrib.admin import widgets  
from django.forms import ModelForm
from runner.models import User
from bus.models import *
from taxi.models import *
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

class RouteForm(forms.Form):
    source = forms.ModelChoiceField(queryset=Stop.objects.all(), to_field_name="name")
    dest = forms.ModelChoiceField(queryset=Stop.objects.all(), to_field_name="name")
    time = forms.DateTimeField()
    token = forms.CharField(label='token', max_length=200)

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
    class Meta:
        model = Booking
        fields = ('user', 'taxi', 'payment_status', 'journey_time', 'source', 'dest')

