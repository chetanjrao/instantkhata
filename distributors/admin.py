from django.contrib import admin
from .models import Distributor, Due, Purchase, Type, District, State, Product, Package, Subscription, Quantity, PaymentMode ,PaymentMethod
# Register your models here.
admin.site.register(Distributor)
admin.site.register(Due)
admin.site.register(Purchase)
admin.site.register(District)
admin.site.register(State)
admin.site.register(Product)
admin.site.register(Package)
admin.site.register(Subscription)
admin.site.register(Type)
admin.site.register(Quantity)
admin.site.register(PaymentMode)
admin.site.register(PaymentMethod)