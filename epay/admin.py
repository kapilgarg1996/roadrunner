from django.contrib import admin
from epay.models import *

admin.site.register(TaxiPayment)
admin.site.register(BusPayment)
admin.site.register(WalletTransaction)
# Register your models here.
