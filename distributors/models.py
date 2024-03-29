from django.db import models
from accounts.models import User, District, State
from django.conf import settings

# Create your models here.
class Distributor(models.Model):
    name = models.CharField(max_length=256)
    logo = models.ImageField(upload_to='uploads/images/', null=True, blank=True)
    gst_number = models.CharField(max_length=32)
    district = models.ForeignKey(to=District, on_delete=models.CASCADE)
    address = models.TextField()
    gst_entity = models.CharField(max_length=32)
    gst_state = models.ForeignKey(to=State, on_delete=models.CASCADE)
    drug_license = models.CharField(max_length=16, null=True, blank=True)
    food_license = models.CharField(max_length=32, null=True, blank=True)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=32)
    distributor = models.ForeignKey(to=Distributor, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to='uploads/products/', null=True, blank=True)
    type = models.ForeignKey(to=Type, on_delete=models.CASCADE)
    distributor = models.ForeignKey(to=Distributor, on_delete=models.CASCADE)
    mrp = models.FloatField()
    hsn = models.CharField(max_length=16)
    base_price = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now=True, null=True)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return '{} - {}'.format(self.name, self.distributor.name)

class Package(models.Model):
    name = models.CharField(max_length=64)
    amount = models.FloatField()
    duration = models.IntegerField(help_text="Total days this packages will work")
    created_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    distributor = models.ForeignKey(to=Distributor, on_delete=models.CASCADE)
    package = models.ForeignKey(to=Package, on_delete=models.CASCADE)
    amount_paid = models.FloatField()
    transaction_id = models.UUIDField(unique=True)
    order_id = models.CharField(max_length=128, unique=True)
    payment_signature = models.CharField(max_length=255, unique=True)
    payment_id =  models.CharField(max_length=128, unique=True)
    payment_date = models.DateField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now=True, null=True)

class Due(models.Model):
    distributor = models.OneToOneField(to=Distributor, on_delete=models.CASCADE)
    subscription = models.ForeignKey(to=Subscription, on_delete=models.CASCADE)
    due_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True, null=True)

class Quantity(models.Model):
    product = models.OneToOneField(to=Product, on_delete=models.CASCADE, related_name='quantity_of_product')
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return "{} - {} units".format(self.product, self.quantity)

class PaymentMode(models.Model):
    name = models.CharField(max_length=512)
    provider = models.ImageField(upload_to='uploads/providers/')

    def __str__(self):
        return self.name


class PaymentMethod(models.Model):
    mode = models.ForeignKey(to=PaymentMode, on_delete=models.CASCADE)
    distributor = models.ForeignKey(to=Distributor, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=512)
    account_id = models.CharField(max_length=128, unique=True)
    is_bank = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    ifsc = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return '{} -> {}'.format(self.distributor.name, self.mode.name)
