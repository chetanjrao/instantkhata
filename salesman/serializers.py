from .models import Salesman, Inventory
from rest_framework import serializers, permissions
from retailers.models import Retailer
from distributors.models import Product, Quantity
from ledger.models import Invoice, Sale, BalanceSheet
from instantkhata import permissions as local_permissions

class SalemanCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Salesman
        fields = '__all__'
    
    def create(self, validated_data):
        return super().create(validated_data)


class InventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventory

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class SalesSerializer(serializers.ModelSerializer):

    permission_classes = [permissions.IsAuthenticated, local_permissions.DistributorPermission, local_permissions.SalesmanPermission]
    
    class Meta:
        model = Sale
        fields = ['quantity', 'product']

    def validate(self, data):
        try:
            quantity_obj = Quantity.objects.get(product=data["product"])
            if quantity_obj.quantity < data["quantity"]:
                raise serializers.ValidationError("Quantity limit exceeded")
            else:
                data["amount"] = data["product"].base_price * data["quantity"]
                return data
        except Quantity.DoesNotExist:
            raise serializers.ValidationError("Quantity does not exist")


    def create(self, validated_data):
        validated_data["salesman"] = self.context.user
        return super().create(validated_data)

class InvoiceSerializer(serializers.ModelSerializer):

    permission_classes = [permissions.IsAuthenticated, local_permissions.DistributorPermission, local_permissions.SalesmanPermission]
    
    class Meta:
        model = Invoice
        fields = '__all__'

    def validate_retailer(self, retailer):
        try:
            retailer = Retailer.objects.get(pk=retailer)
            return retailer
        except Retailer.DoesNotExist:
            raise serializers.ValidationError("Retailer does not exist")
    
