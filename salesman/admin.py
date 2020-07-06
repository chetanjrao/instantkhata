from django.contrib import admin
from .models import Salesman, Inventory
# Register your models here.

class SalesmanAdmin(admin.ModelAdmin):
    filter_horizontal = ('distributor', )

admin.site.register(Salesman, SalesmanAdmin)
admin.site.register(Inventory)