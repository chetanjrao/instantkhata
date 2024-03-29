from rest_framework import serializers, validators, fields
from .models import Distributor, State, District, Due, Subscription, Package, Product, Quantity as Qty, Type, PaymentMode, PaymentMethod
from logs.models import Quantity
from django.utils import timezone
from salesman.models import Salesman, Inventory
from retailers.models import Retailer, Request
from ledger.models import Invoice, BalanceSheet, Balance
from uuid import uuid4
from django.utils.timezone import now, timedelta

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


class InventorySerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField()

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        quantity = Qty.objects.create(product=product, quantity=validated_data["quantity"])
        quantity_log = Quantity.objects.create(product=product, type='A', quantity=validated_data["quantity"], remarks="Added items to the inventory", updated_by=validated_data["distributor"].user)
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
            return product
        except Product.DoesNotExist:
            raise validators.ValidationError("Product is not associated or does not exist")

    def validate_salesman(self, salesman):
        try:
            salesman_obj = Salesman.objects.get(pk=salesman)
            return salesman_obj
        except Salesman.DoesNotExist:
            raise validators.ValidationError("Salesman does not exist")

    def validate_quantity(self, quantity):
        try:
            quantity_check = Qty.objects.get(product=self.initial_data["product"])
            if quantity <= quantity_check.quantity:
                return quantity
            else:
                raise validators.ValidationError("Product quantity exceeded")
        except Qty.DoesNotExist:
            raise validators.ValidationError("Invalid product")


    def create(self, validated_data):
        try:
            salesman_inventory = Inventory.objects.get(salesman=validated_data["salesman"].pk, product=validated_data["product"])
            salesman_inventory.quantity = salesman_inventory.quantity + validated_data["quantity"]
            salesman_inventory.save()
            current_quantity = Qty.objects.get(product=self.validated_data["product"])
            current_quantity.quantity = current_quantity.quantity - validated_data["quantity"]
            current_quantity.save()
            return salesman_inventory
        except Inventory.DoesNotExist:
            new_inventory = Inventory(salesman=self.validated_data["salesman"].pk, product=self.validated_data["product"], quantity=self.validated_data["quantity"])
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

class PaymentModeSerializer(serializers.ModelSerializer):
    image = serializers.ReadOnlyField(source='provider.url')

    class Meta:
        model = PaymentMode
        fields = ('name', 'image')


class PaymentMethodListSerializer(serializers.ModelSerializer):
    mode = serializers.ReadOnlyField(source='mode.name')
    image = serializers.ReadOnlyField(source='mode.provider.url')
    class Meta:
        model = PaymentMethod
        fields = ('mode', 'image', 'account_name', 'account_id', 'is_bank', 'ifsc')


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ('mode', 'account_name', 'account_id', 'is_bank', 'ifsc')

    def create(self, validated_data):
        validated_data["distributor"] = Distributor.objects.get(user=self.context["user"])
        return super().create(validated_data)


class PackageListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Package
        fields = ('name', 'amount', 'duration')


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('package', 'amount_paid', 'order_id', 'payment_id', 'payment_signature')


    def validate_amount_paid(self, amount_paid):
        package = Package.objects.get(id=self.initial_data["package"])
        if amount_paid != package.amount:
            raise serializers.ValidationError("Invalid amount request")
        return amount_paid

    def create(self, validated_data):
        distributor = Distributor.objects.get(user=self.context["user"])
        validated_data["distributor"] = distributor
        validated_data["transaction_id"] = uuid4()
        package = validated_data["package"]
        due_cal = now() + timedelta(days=package.duration)
        subscription = Subscription.objects.create(**validated_data)
        try:
            due_details = Due.objects.get(distributor=distributor)
            due_details.subscription = subscription
            new_due_cal = due_cal + timedelta(days=package.duration)
            due_details.due_date = new_due_cal
            due_details.updated_at = now()
            due_details.save()
        except Due.DoesNotExist:
            new_due_date = Due.objects.create(distributor=distributor, subscription=subscription, due_date=due_cal)
        return subscription


class TransactionListSerializer(serializers.ModelSerializer):
    retailer = serializers.ReadOnlyField(source='retailer.name')
    payment_name = serializers.ReadOnlyField(source='payment_mode.mode.name')
    payment_image = serializers.ReadOnlyField(source='payment_mode.mode.provider.url')
    uid = serializers.ReadOnlyField(source='invoice.uid')
    
    class Meta:
        model = BalanceSheet
        fields = ('retailer', 'id', 'payment_name', 'payment_image', 'amount', 'uid', 'invoice', 'closing_balance', 'is_credit', 'created_at')


class BalanceSheetListSerializer(serializers.ModelSerializer):
    image = serializers.ReadOnlyField(source='payment_mode.mode.provider.url')

    class Meta:
        model = BalanceSheet
        fields = ('id', 'amount', 'is_credit', 'image', 'created_at', )

