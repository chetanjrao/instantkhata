from .models import Salesman, Inventory
from rest_framework import serializers, permissions
from retailers.models import Retailer
from distributors.models import Distributor, Product, Quantity, PaymentMethod
from ledger.models import Invoice, Sale, BalanceSheet, Balance
from instantkhata import permissions as local_permissions
from django.utils.timezone import now
from salesman.models import Inventory
from uuid import uuid4
from logs.models import Quantity as logQty
from math import ceil

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
        fields = ['quantity', 'product', 'discount', 'tax']

    def validate(self, data):
        try:
            data["tax"] = data.get("tax", 18)
            quantity_obj = Inventory.objects.get(product=data["product"], salesman__user=self.context["user"])
            if quantity_obj.quantity < data["quantity"]:
                raise serializers.ValidationError("Quantity limit exceeded")
            else:
                data["taxable_value"] = data["product"].base_price * data["quantity"]
                data["amount"] = data["taxable_value"] + (data["tax"] * data["taxable_value"] / 100) - (data["discount"] * data["taxable_value"] / 100)
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

    def validate_distributor(self, distributor):
        check_distributor = Salesman.objects.get(user=self.context["user"])
        current_distributor = Distributor.objects.get(pk=distributor.pk)
        if current_distributor in check_distributor.distributor.all():
            return current_distributor
        else:
            raise serializers.ValidationError("Distributor not associated")

    def create(self, validated_data):
        validated_data["salesman"] = Salesman.objects.get(user=self.context["user"])
        validated_data["payment_id"] = validated_data["payment_mode"].account_id
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
        new_balance_sheet = BalanceSheet(invoice=new_invoice, opening_balance=current_balance.closing_balance, closing_balance=current_balance.closing_balance+final_amount-validated_data["amount_paid"], payment_mode=validated_data["payment_mode"], payment_id=validated_data["payment_id"], created_by=validated_data["salesman"], retailer=validated_data["retailer"], distributor=validated_data["distributor"], amount=validated_data["amount_paid"], remaining_balance=final_amount - validated_data["amount_paid"])
        current_balance.opening_balance = current_balance.closing_balance
        current_balance.closing_balance = current_balance.closing_balance + final_amount - validated_data["amount_paid"]
        current_balance.last_updated_by = now()
        current_balance.save()
        new_balance_sheet.save()
        return new_invoice
    

class InvoiceUpdateSerializer(serializers.Serializer):
    invoice = serializers.CharField(max_length=100)
    amount = serializers.FloatField()
    payment_mode = serializers.IntegerField()
    deadline = serializers.DateField()

    permission_classes = [permissions.IsAuthenticated, local_permissions.DistributorPermission, local_permissions.SalesmanPermission]


    def validate_invoice(self, invoice):
        invoice = Invoice.objects.get(uid=invoice)
        if ceil(invoice.balance) >= self.initial_data["amount"] and self.initial_data["amount"] > 0:
            return invoice
        else:
            raise serializers.ValidationError("Amount exceeded remaining balance")

    def validate_payment_mode(self, payment_mode):
        try:
            payment_mode = PaymentMethod.objects.get(pk=payment_mode)
            return payment_mode
        except PaymentMethod.DoesNotExist:
            raise serializers.ValidationError("Payment mode does not exist")


    def create(self, validated_data):
        invoice = validated_data["invoice"]
        current_balance = Balance.objects.get(retailer=invoice.retailer, distributor=invoice.distributor)
        new_balance_sheet = BalanceSheet(
            invoice = invoice,
            opening_balance = current_balance.closing_balance,
            closing_balance = current_balance.closing_balance - validated_data["amount"],
            amount = validated_data["amount"],
            is_credit=False,
            remaining_balance=invoice.balance - validated_data["amount"] if invoice.balance - validated_data["amount"] > 0 else 0,
            payment_mode=validated_data["payment_mode"],
            payment_id=validated_data["payment_mode"].account_id,
            created_by = Salesman.objects.get(user=self.context["user"]),
            retailer=invoice.retailer,
            distributor=invoice.distributor
        )
        invoice.balance = invoice.balance - validated_data["amount"] if invoice.balance - validated_data["amount"] > 0 else 0
        invoice.deadline = validated_data["deadline"]
        invoice.last_updated_at = now()
        invoice.save()
        current_balance.opening_balance = current_balance.closing_balance
        current_balance.closing_balance = current_balance.closing_balance - validated_data["amount"]
        current_balance.last_updated_by = now()
        current_balance.save()
        new_balance_sheet.save()
        return invoice


class BalanceSheetListSerializer(serializers.ModelSerializer):

    permission_classes = [permissions.IsAuthenticated, local_permissions.DistributorPermission, local_permissions.SalesmanPermission]

    class Meta:
        model = BalanceSheet
        fields = ('id', 'amount', 'is_credit', 'created_at', )


class InvoiceListSerializer(serializers.ModelSerializer):

    permission_classes = [permissions.IsAuthenticated, local_permissions.DistributorPermission, local_permissions.SalesmanPermission]

    class Meta:
        model = Invoice
        fields = ('total_amount', 'uid', 'created_at', 'retailer')