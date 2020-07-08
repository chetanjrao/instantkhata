from django.db import models
from salesman.models import Salesman
from distributors.models import Distributor, Product
from retailers.models import Retailer
import uuid

# Create your models here.
class Sale(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    sch = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    tax = models.FloatField(default=18)
    box = models.FloatField(default=0)
    taxable_value = models.FloatField()
    created_at = models.DateTimeField(auto_now=True, null=True)
    amount = models.FloatField()


class Invoice(models.Model):
    sales = models.ManyToManyField(to=Sale)
    salesman = models.ForeignKey(to=Salesman, on_delete=models.CASCADE)
    retailer = models.ForeignKey(to=Retailer, on_delete=models.CASCADE)
    distributor = models.ForeignKey(to=Distributor, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    amount_paid = models.FloatField()
    payment_mode = models.CharField(max_length=16)
    balance = models.FloatField()
    uid = models.CharField(max_length=32, unique=True, default=uuid.uuid4().hex)
    deadline = models.DateField()
    last_updated_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now=True, null=True)


class BalanceSheet(models.Model):
    invoice = models.ForeignKey(to=Invoice, on_delete=models.CASCADE)
    opening_balance = models.FloatField()
    amount = models.FloatField()
    closing_balance = models.FloatField()
    is_credit = models.BooleanField(default=True)
    payment_mode = models.CharField(max_length=16)
    created_by = models.ForeignKey(to=Salesman, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, null=True)
    retailer = models.ForeignKey(to=Retailer, on_delete=models.CASCADE)
    distributor = models.ForeignKey(to=Distributor, on_delete=models.CASCADE)


class Balance(models.Model):
    opening_balance = models.FloatField(default=0)
    closing_balance = models.FloatField(default=0)
    retailer = models.ForeignKey(to=Retailer, on_delete=models.CASCADE)
    distributor = models.ForeignKey(to=Distributor, on_delete=models.CASCADE)
    last_updated_by = models.DateTimeField(auto_now=True)