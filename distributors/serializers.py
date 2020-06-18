from rest_framework import serializers
from .models import Distributor, State, District, Purchase, Due, Subscription, Package


class DistributorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Distributor
        fields = ('name', 'gst_number', 'district', 'address', 'gst_entity', 'gst_state', 'drug_license', 'food_license', 'user')

    def create(self, validated_data:dict):
        state = State.objects.get(pk=validated_data["state"])
        district = District.objects.get(pk=validated_data["district"])
        validated_data["state"], validated_data["district"] = state, district
        return Distributor(**validated_data)

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