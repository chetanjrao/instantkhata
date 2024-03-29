from django.shortcuts import render, HttpResponse
from .serializers import SalesSerializer, InvoiceSerializer, InvoiceUpdateSerializer, BalanceSheetListSerializer, PaymentMethodListSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ledger.models import Sale, Invoice, BalanceSheet
from distributors.models import PaymentMethod, Type
from distributors.views import createMessage
from django.utils.timezone import now, timedelta, datetime, localtime
from django.db.models import Sum, F
from .models import Salesman, Inventory
from instantkhata import permissions
from rest_framework import permissions as main_permissions
from retailers.models import Retailer
from distributors.serializers import TypeCreationSerializer
# Create your views here.


class SalesCreationView(APIView):

    def post(self, request, *args, **kwargs):
        sales_seralizer = SalesSerializer(data=request.data, many=True)
        if sales_seralizer.is_valid():
            return Response(sales_seralizer.data)
        else:
            return Response(sales_seralizer.errors)

    def get_queryset(self):
        return Sale.objects.all()


class InvoiceCreationView(APIView):

    def post(self, request, *args, **kwargs):
        invoice_seralizer = InvoiceSerializer(data=request.data, context={
            "user": request.user
        })
        if invoice_seralizer.is_valid():
            new_invoice = invoice_seralizer.save()
            return Response(createMessage("Invoice created successfully", 200))
        else:
            return Response(invoice_seralizer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return Sale.objects.all()

class InvoiceEditView(APIView):

    def post(self, request, *args, **kwargs):
        invoice_serializer = InvoiceUpdateSerializer(data=request.data, context={
            "user": request.user
        })
        if invoice_serializer.is_valid():
            invoice_serializer.save()
            return Response(createMessage("Invoice updated succesfully", 200))
        else:
            return Response(invoice_serializer.errors, status=400)

    def get_queryset(self):
        return Invoice.objects.all()

class SalesmanAnalyticsView(APIView):

    def post(self, request, *args, **kwargs):
        today = localtime()
        month_start = today.replace(day=1, second=0, minute=0, hour=0, microsecond=0)
        prev_month_end = (today.replace(day=1, second=59, minute=59, hour=23) - timedelta(days=1))
        prev_month_start = prev_month_end.replace(day=1, second=0, minute=0, hour=0)
        current_sales = Invoice.objects.filter(salesman=Salesman.objects.get(user=request.user), distributor=request.data["distributor"], created_at__gte=month_start, created_at__lte=today).aggregate(sales=Sum('total_amount'))
        previous_sales = Invoice.objects.filter(salesman=Salesman.objects.get(user=request.user), distributor=request.data["distributor"], created_at__gte=prev_month_start, created_at__lte=prev_month_end).aggregate(sales=Sum('total_amount'))
        if previous_sales["sales"] is None:
            previous_sales["sales"] = 0
        if current_sales["sales"] is None:
            current_sales["sales"] = 0
        return Response({
            "status": (current_sales["sales"] - previous_sales["sales"]) * 100 / previous_sales["sales"] if previous_sales["sales"] else current_sales["sales"],
            "total": current_sales["sales"]
        })
        #current_analytics = Invoice.objects.filter(created_at__lte=now,)

    def get_queryset(self):
        return Invoice.objects.all()


class TransactionList(APIView):

    def post(self, request, *args, **kwargs):
        today = localtime()
        month_start = today.replace(day=1, second=0, minute=0, hour=0, microsecond=0)
        transactions = BalanceSheet.objects.filter(created_by=Salesman.objects.get(user=request.user), distributor=request.data["distributor"], created_at__gte=month_start, created_at__lte=today).order_by('-created_at')
        serializer = BalanceSheetListSerializer(transactions, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return BalanceSheet.objects.all()

class AllTransactionList(APIView):

    def post(self, request, *args, **kwargs):
        transactions = BalanceSheet.objects.filter(created_by=Salesman.objects.get(user=request.user), distributor=request.data["distributor"]).order_by('-created_at')
        serializer = BalanceSheetListSerializer(transactions, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return BalanceSheet.objects.all()


class RetailersListView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            retailers = Retailer.objects.filter(distributors__pk=request.GET["distributor"]).values('id', 'name', 'latitude', 'longitude', 'address' ,mobile=F('user__mobile'))
            return Response(retailers)
        except (KeyError, Retailer.DoesNotExist):
            return Response(createMessage("Bad Request", 400), status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return Retailer.objects.all()


class InventoryListView(APIView):

    def post(self, request, *args, **kwargs):
        inventory = Inventory.objects.filter(salesman__user=request.user, product__distributor=request.data["distributor"]).values('product_id', 'quantity', type= F('product__type'), name=F('product__name'), mrp=F('product__mrp'), base_price=F('product__base_price'))
        return Response(inventory)


    def get_queryset(self):
        return Inventory.objects.all()


class TypesView(APIView):

    permission_classes = [main_permissions.IsAuthenticated, permissions.DistributorPermission, permissions.SalesmanPermission]

    def post(self, request, *args, **kwargs):
        data = Type.objects.filter(distributor=request.data["distributor"])
        serializer = TypeCreationSerializer(data, many=True)
        return Response(serializer.data)



class InvoiceListView(APIView):

    def post(self, request):
        invoices = Invoice.objects.filter(distributor__pk=request.data["distributor"], salesman__user=request.user).values('total_amount', 'uid', 'retailer__name', 'created_at').order_by('-created_at')
        return Response(invoices)

    def get_queryset(self):
        return Invoice.objects.all()


class TransactionView(APIView):

    def post(self, request, t_id):
        transactions = BalanceSheet.objects.filter(pk=t_id).values('retailer__name', 'amount', 'payment_mode', 'is_credit', 'created_at', 'invoice__uid')
        return Response(transactions)

    def get_queryset(self):
        return Invoice.objects.all()

class PaymentListView(APIView):

    def post(self, request):
        payment_methods = PaymentMethod.objects.filter(distributor=request.data["distributor"], is_deleted=False)
        serializer = PaymentMethodListSerializer(payment_methods, many=True)
        return Response(serializer.data)


    def get_queryset(self):
        return PaymentMethod.objects.all()
    


class Distributors(APIView):
   

    def get(self, request):
        try:
            distributors = Salesman.objects.get(user=request.user).distributor.all().values('id', 'name', 'address')
            return Response(distributors)
        except Salesman.DoesNotExist:
            return Response(createMessage("Invalid Request", 400), status=status.HTTP_400_BAD_REQUEST)

    
    def get_queryset(self):
        return Salesman.objects.all()

def invoice_view(request, invoice):
    try:
        invoice = Invoice.objects.get(uid=invoice)
        amount = 0
        for sale in invoice.sales.all():
            amount += sale.taxable_value
        balance_sheet = BalanceSheet.objects.filter(invoice=invoice).order_by('-created_at')
        return render(request, "invoice.html", { "invoice": invoice, "balance_sheets": balance_sheet, "amount": amount })
    except Invoice.DoesNotExist:
        return HttpResponse("Requested entity does not exist", status=status.HTTP_404_NOT_FOUND)
