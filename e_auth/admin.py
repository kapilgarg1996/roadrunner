from django.contrib import admin
from django.conf import settings
import e_auth

class AuthAdmin(admin.ModelAdmin):
    list_display = ('get_user_data', 'auth_token', 'create_time', 'expire_time')

admin.site.register(e_auth.models.Authorize, AuthAdmin)
# Register your models here.
