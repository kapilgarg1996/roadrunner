from django import forms
from django.contrib.admin import widgets  
from django.forms import ModelForm
from runner.models import User
from bus.models import *
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

class UserSignupForm(ModelForm):
    class Meta:
        model = User
        exclude = ('id',)
