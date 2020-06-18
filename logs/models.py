from django.db import models
from accounts.models import User
from distributors.models import Product

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
