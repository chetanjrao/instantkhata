from django.db import models
from accounts.models import User
from distributors.models import Distributor, Product
# Create your models here.
class Salesman(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    distributor = models.ManyToManyField(to=Distributor)

class Inventory(models.Model):
    salesman = models.ForeignKey(to=Salesman, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
