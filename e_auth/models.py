from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.conf import settings
import importlib

setlist = settings.EAUTH_USER.split('.')
UserApp = importlib.import_module('.'.join(setlist[:-1]))
User = getattr(UserApp, setlist[-1])

@python_2_unicode_compatible
class Authorize(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE, related_name='+', default='')
    auth_token = models.CharField(max_length=200, default='')
    create_time = models.DateTimeField()
    expire_time = models.DateTimeField()

    def get_user_data(self):
        return getattr(self.user,settings.EAUTH_FIELDS[0])

    get_user_data.short_description = 'User'
    def __str__(self):
        field = settings.EAUTH_FIELDS[0]
        return getattr(self.user, field)
# Create your models here.
