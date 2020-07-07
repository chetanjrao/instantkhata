from .models import Salesman, Inventory
from rest_framework import serializers, permissions
from retailers.models import Retailer
from distributors.models import Product, Quantity
from ledger.models import Invoice, Sale, BalanceSheet, Balance
from instantkhata import permissions as local_permissions
from django.utils.timezone import now
from salesman.models import Inventory
from uuid import uuid4

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
            print(data["product"])
            quantity_obj = Inventory.objects.get(product=data["product"], salesman__user=self.context["user"])
            if quantity_obj.quantity < data["quantity"]:
                raise serializers.ValidationError("Quantity limit exceeded")
            else:
                data["amount"] = data["product"].base_price * data["quantity"]
                return data
        except Inventory.DoesNotExist:
            raise serializers.ValidationError("Product does not exist")


    def create(self, validated_data):
        return super().create(validated_data)


class InvoiceSerializer(serializers.ModelSerializer):
    sales = SalesSerializer(many=True)
    permission_classes = [permissions.IsAuthenticated, local_permissions.DistributorPermission, local_permissions.SalesmanPermission]
    
    class Meta:
        model = Invoice
        fields = ('sales', 'retailer', 'distributor', 'total_amount', 'amount_paid', 'payment_mode', 'deadline', 'last_updated_at')

    def create(self, validated_data):
        validated_data["salesman"] = Salesman.objects.get(user=self.context["user"])
        new_sales = validated_data.pop("sales")
        final_amount = 0
        validated_data["uid"] = uuid4().hex
        validated_data["balance"] = 0
        new_invoice = Invoice(**validated_data)
        new_invoice.save()
        for sale in new_sales:
            curr_sale = Sale.objects.create(**sale)
            new_invoice.sales.add(curr_sale)
            curr_inventory = Inventory.objects.get(salesman=validated_data["salesman"], product=sale["product"])
            curr_inventory.quantity = curr_inventory.quantity - sale["quantity"]
            curr_inventory.save()
            final_amount += sale["amount"]
        new_invoice.total_amount = final_amount
        new_invoice.balance = final_amount - validated_data["amount_paid"]
        new_invoice.save()
        current_balance = Balance.objects.get(retailer=validated_data["retailer"], distributor=validated_data["distributor"])
        current_balance.opening_balance = current_balance.closing_balance
        current_balance.closing_balance = current_balance.closing_balance + final_amount - validated_data["amount_paid"]
        current_balance.last_updated_by = now()
        current_balance.save()
        new_balance_sheet = BalanceSheet(invoice=new_invoice, opening_balance=current_balance.closing_balance, closing_balance=current_balance.closing_balance+final_amount-validated_data["amount_paid"], payment_mode=validated_data["payment_mode"], created_by=validated_data["salesman"], retailer=validated_data["retailer"], distributor=validated_data["distributor"], amount=final_amount - validated_data["amount_paid"])
        new_balance_sheet.save()
        return new_invoice
    
