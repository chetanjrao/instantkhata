from rest_framework import serializers
from .models import Distributor, State, District, Purchase, Due, Subscription, Package, Product, Quantity as Qty
from logs.models import Quantity
from django.utils import timezone

class DistributorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Distributor
        fields = ('name', 'gst_number', 'district', 'address', 'gst_entity', 'gst_state', 'drug_license', 'food_license', 'user')

    def create(self, validated_data:dict):
        state = State.objects.get(pk=validated_data["state"])
        district = District.objects.get(pk=validated_data["district"])
        validated_data["state"], validated_data["district"] = state, district
        return Distributor(**validated_data)

    def update(self, instance:Distributor, validated_data:dict):
        instance.name = validated_data.get(validated_data['name'], instance.name)
        instance.save()
        return instance

class PurchaseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Purchase
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)


class DueDateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Due
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'


class InventorySerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField()

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        product.save()
        quantity = Qty.objects.create(product=product, quantity=validated_data["quantity"])
        quantity.save()
        quantity_log = Quantity.objects.create(product=product, type='A', quantity=validated_data["quantity"], remarks="Added items to the inventory", updated_by=validated_data["distributor"].user)
        quantity_log.save()
        return super().create(validated_data)