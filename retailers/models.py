from django.db import models
from accounts.models import User, District, State
from distributors.models import Distributor, Product

# Create your models here.
class Retailer(models.Model):
    name = models.CharField(max_length=256)
    logo = models.ImageField(upload_to='uploads/images/')
    gst_number = models.CharField(max_length=32)
    district = models.ForeignKey(to=District, on_delete=models.CASCADE)
    address = models.TextField()
    gst_entity = models.CharField(max_length=32)
    gst_state = models.ForeignKey(to=State, on_delete=models.CASCADE)
    food_license = models.CharField(max_length=32, null=True, blank=True)
    drug_license = models.CharField(max_length=16, null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    distributors = models.ManyToManyField(to=Distributor)

    def __str__(self):
        return self.name

class Request(models.Model):
    CHOICES = (
        (0, 'Pending'),
        (1, 'Approved'),
        (2, 'Cancelled'),
    )
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    retailer = models.ForeignKey(to=Retailer, on_delete=models.CASCADE)
    distributor = models.ForeignKey(to=Distributor, on_delete=models.CASCADE)
    quantity = models.IntegerField(choices=CHOICES, default=0)
    status = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True, null=True)