from django.db import models
from salesman.models import Salesman
from distributors.models import Product
from retailers.models import Retailer

# Create your models here.
class Sale(models.Model):
    salesman = models.ForeignKey(to=Salesman, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True, null=True)
    amount = models.FloatField()


class Invoice(models.Model):
    sales = models.ManyToManyField(to=Sale)
    retailer = models.ForeignKey(to=Retailer, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    amount_paid = models.FloatField()
    payment_mode = models.CharField(max_length=16)
    balance = models.FloatField()
    deadline = models.DateField()
    last_updated_at = models.DateTimeField(auto_now=True, null=True)


class BalanceSheet(models.Model):
    invoice = models.ForeignKey(to=Invoice, on_delete=models.CASCADE)
    opening_balance = models.FloatField()
    amount = models.FloatField()
    closing_balance = models.FloatField()
    payment_mode = models.CharField(max_length=16)
    created_by = models.ForeignKey(to=Salesman, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, null=True)