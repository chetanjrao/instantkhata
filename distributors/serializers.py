from rest_framework import serializers, validators, fields
from .models import Distributor, State, District, Purchase, Due, Subscription, Package, Product, Quantity as Qty, Type
from logs.models import Quantity
from django.utils import timezone
from salesman.models import Salesman, Inventory
from retailers.models import Retailer, Request
from ledger.models import Invoice, BalanceSheet, Balance

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

class BaseInventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'image', 'type', 'mrp', 'hsn', 'base_price')

    def get_queryset(self):
        return Product.objects.filter(distributor__user=self.request.user)


class BaseTypeView(serializers.ModelSerializer):

    class Meta:
        model = Type
        fields = ('name')

    def create(self, validated_data):
        return super().create(validated_data)


class TypeCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Type
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)

    def get_queryset(self):
        return Type.objects.filter(distributor__user=self.request.user)


class SalesmanSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.first_name', read_only=True)
    mobile = serializers.CharField(source='user.mobile', read_only=True)


    class Meta:
        model = Salesman
        fields = ( 'id', 'name', 'mobile')


class SalesmanTransferSerializer(serializers.Serializer):
    salesman = serializers.IntegerField()
    product = serializers.IntegerField()
    quantity = serializers.IntegerField()

    def validate_product(self, product):
        try:
            user = self.context["user"]
            distributor = Distributor.objects.get(user=user)
            product = Product.objects.get(pk=product, distributor=distributor)
            self.product = product
            return product
        except Product.DoesNotExist:
            raise validators.ValidationError("Product is not associated or does not exist")

    def validate_salesman(self, salesman):
        try:
            salesman_obj = Salesman.objects.get(pk=salesman)
            self.salesman = salesman_obj
            return salesman_obj
        except Salesman.DoesNotExist:
            raise validators.ValidationError("Salesman does not exist")

    def validate_quantity(self, quantity):
        try:
            quantity_check = Qty.objects.get(product=self.product)
            if quantity <= quantity_check.quantity:
                return quantity
            else:
                raise validators.ValidationError("Product quantity exceeded")
        except Qty.DoesNotExist:
            raise validators.ValidationError("Invalid product")


    def create(self, validated_data):
        try:
            salesman_inventory = Inventory.objects.get(salesman=self.validated_data["salesman"], product=self.validated_data["product"])
            salesman_inventory.quantity = salesman_inventory.quantity + quantity
            print(salesman_inventory)
            salesman_inventory.save()
            current_quantity = Qty.objects.get(product=self.validated_data["product"])
            current_quantity.quantity = current_quantity.quantity - self.validated_data["quantity"]
            current_quantity.save()
            return salesman_inventory
        except Inventory.DoesNotExist:
            new_inventory = Inventory(salesman=self.validated_data["salesman"], product=self.validated_data["product"], quantity=self.validated_data["quantity"])
            new_inventory.save()
            current_quantity = Qty.objects.get(product=self.validated_data["product"])
            current_quantity.quantity = current_quantity.quantity - self.validated_data["quantity"]
            current_quantity.save()
            return new_inventory

    def update(self, instance, validated_data):
        return instance


class SalesmanAddSerializer(serializers.Serializer):
    salesman = serializers.IntegerField()

    def validate_salesman(self, salesman):
        try:
            salesman = Salesman.objects.get(pk=salesman)
            return salesman
        except Salesman.DoesNotExist:
            raise serializers.ValidationError("Salesman does not exist")

    def create(self, validated_data):
        user = self.context["user"]
        distributor = Distributor.objects.get(user=user)
        salesman = self.validated_data["salesman"]
        salesman.distributor.add(distributor)
        return salesman

class SalesmanDeleteSerializer(serializers.Serializer):
    salesman = serializers.IntegerField()

    def validate_salesman(self, salesman):
        try:
            salesman = Salesman.objects.get(pk=salesman)
            return salesman
        except Salesman.DoesNotExist:
            raise serializers.ValidationError("Salesman does not exist")

    def create(self, validated_data):
        user = self.context["user"]
        distributor = Distributor.objects.get(user=user)
        salesman = self.validated_data["salesman"]
        salesman.distributor.remove(distributor)
        return salesman


class RetailerAddSerializer(serializers.Serializer):
    retailer = serializers.IntegerField()
    opening_balance = serializers.FloatField()

    def validate_retailer(self, retailer):
        try:
            retailer = Retailer.objects.get(pk=retailer)
            return retailer
        except Retailer.DoesNotExist:
            raise serializers.ValidationError("Retailer does not exist")

    def create(self, validated_data):
        user = self.context["user"]
        distributor = Distributor.objects.get(user=user)
        retailer = self.validated_data["retailer"]
        try:
            check_balance = Balance.objects.get(retailer=retailer, distributor=distributor)
        except Balance.DoesNotExist:
            Balance.objects.create(retailer=retailer, distributor=distributor, opening_balance=validated_data["opening_balance"], closing_balance=validated_data["opening_balance"])
        retailer.distributors.add(distributor)
        return retailer


class RetailerDeleteSerializer(serializers.Serializer):
    retailer = serializers.IntegerField()

    def validate_retailer(self, retailer):
        try:
            retailer = Retailer.objects.get(pk=retailer)
            return retailer
        except Retailer.DoesNotExist:
            raise serializers.ValidationError("Retailer does not exist")

    def create(self, validated_data):
        user = self.context["user"]
        distributor = Distributor.objects.get(user=user)
        retailer = self.validated_data["retailer"]
        retailer.distributors.remove(distributor)
        return retailer
