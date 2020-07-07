from django.contrib import admin
from .models import Sale, Invoice, Balance, BalanceSheet
# Register your models here.
admin.site.register(Sale)
admin.site.register(Invoice)
admin.site.register(BalanceSheet)
admin.site.register(Balance)