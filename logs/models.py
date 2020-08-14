from django.db import models
from accounts.models import User
from distributors.models import Distributor, Product
from retailers.models import Retailer

# Create your models here.
class Quantity(models.Model):
    LOG_TYPES = (
        ('A', 'ADDITION'),
        ('D', 'DELETION'),
        ('T', 'TRANSFER')
    )
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=LOG_TYPES)
    quantity = models.IntegerField()
    remarks = models.TextField()
    updated_by = models.ForeignKey(to=User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class Notifications(models.Model):
    TYPES = (
        ('B', 'Balance Notification'),
        ('I', 'Invoice Notification')
    )
    retailer = models.ForeignKey(to=Retailer, on_delete=models.PROTECT)
    type = models.CharField(max_length=1, choices=TYPES)
    entity = models.IntegerField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    distributor = models.ForeignKey(to=Distributor, on_delete=models.PROTECT)

class Messages(models.Model):
    title = models.CharField(max_length=512)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    distributor = models.ForeignKey(to=Distributor, on_delete=models.PROTECT)
