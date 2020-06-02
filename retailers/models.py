from django.db import models
from accounts.models import User, District, State
from distributors.models import Distributor

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