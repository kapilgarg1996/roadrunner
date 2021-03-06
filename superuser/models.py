from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.db import connection
from superuser.forms import *
def get_user_file(instance, filename):
    return 'users/{0}_{1}_{2}'.format(instance.name, instance.email, filename)

#-----Model Class Initialization-------------
from django.conf import settings
import importlib

setlist = settings.SUPERUSER_USER.split('.')
UserApp = importlib.import_module('.'.join(setlist[:-1]))
User = getattr(UserApp, setlist[-1])
#-------------------------------------------
@python_2_unicode_compatible
class Validation(models.Model):
    key = models.AutoField(primary_key=True)
    key_data = models.CharField(max_length=100, default='')
    create_time = models.DateTimeField()
    expire_time = models.DateTimeField()
    
    def __str__(self):
        return self.key_data

@python_2_unicode_compatible
class UserTemp(User):    

    validation_key = models.ForeignKey(Validation, models.SET_NULL, related_name='+', null=True, blank=True)  # Field name made lowercase.
    verified = models.BooleanField(default=False)
    def __str__(self):
        primary = settings.SUPERUSER_PRIMARY
        return getattr(self, primary)

    def to_dict(self):
        form = FormTemp()
        formlist = form.fields.keys()
        selflist = self._meta.get_fields()
        data = {}
        for field in selflist:
            if field.name in formlist:
                data[field.name] = getattr(self, field.name)
        return data


@python_2_unicode_compatible
class PassRequest(models.Model):
    user = models.ForeignKey(UserTemp, models.DO_NOTHING, default='', related_name='+')
    validation_key = models.ForeignKey(Validation, models.SET_NULL, related_name='+', null=True, blank=True)  # Field name made lowercase.
    pending = models.BooleanField(default=True)
    request_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return getattr(self.user, settings.SUPERUSER_PRIMARY)
