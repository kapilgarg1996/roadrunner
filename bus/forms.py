from django import forms
from bus.models import Stop
from django.contrib.admin import widgets  
from django.forms import ModelForm


class RouteForm(forms.Form):
    source = forms.ModelChoiceField(queryset=Stop.objects.all(), to_field_name="name")
    dest = forms.ModelChoiceField(queryset=Stop.objects.all(), to_field_name="name")
    time = forms.DateTimeField()

