from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from .serializers import (DistributorSerializer, InventorySerializer, 
    BaseInventorySerializer, TypeCreationSerializer, SalesmanSerializer, 
    SalesmanTransferSerializer, SalesmanAddSerializer, 
    SalesmanDeleteSerializer, RetailerAddSerializer, 
    RetailerDeleteSerializer, PaymentModeSerializer, PaymentMethodSerializer,
    PaymentMethodListSerializer
    )
from rest_framework.response import Response
from instantkhata import permissions as local_permissions
from instantkhata.utils import createMessage, send_message
from rest_framework import status
from .models import Product, Type, Distributor, PaymentMode, PaymentMethod
from salesman.models import Salesman, Inventory
from ledger.models import Invoice, BalanceSheet, Balance
from django.utils.timezone import localtime, datetime, timedelta, now
from django.db.models import Sum, F
from retailers.models import Retailer, Request
from logs.models import Notifications

# Create your views here.
class DistributorRegistration(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = DistributorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


    def patch(self, request, *args, **kwargs):
        """
        Verify payment signature here and proceed updation
        """
        return Response("Welcome")

class InventoryListView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(distributor__user=request.user)
        serializer = BaseInventorySerializer(products, many=True)
        return Response(serializer.data)

class InventoryCreationView(APIView):

    permission_classes = [permissions.IsAuthenticated, local_permissions.DistributorPermission]

    def post(self, request, *args, **kwargs):
        request.data["distributor"] = request.user.pk
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(createMessage("Item added successfully", status.HTTP_200_OK))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BaseCategoryView(APIView):
    
    permission_classes = [permissions.IsAuthenticated, local_permissions.DistributorPermission]

    def post(self, request, *args, **kwargs):
        request.data["distributor"] = request


class BaseDistributorView(RetrieveAPIView):

    def get_queryset(self):
        return super().get_queryset()


class TypeCreationView(APIView):

    permission_classes = [permissions.IsAuthenticated, local_permissions.DistributorPermission]

    def post(self, request, *args, **kwargs):
        request.data["distributor"] = Distributor.objects.get(user=request.user).pk
        print(request.data)
        serilizer = TypeCreationSerializer(data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(createMessage("Category created successfully", 200))
        else:
            return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        data = Type.objects.filter(distributor__user=request.user)
        serializer = TypeCreationSerializer(data, many=True)
        return Response(serializer.data)

class SalesmanListSerializer(APIView):

    permission_classes = [permissions.IsAuthenticated, local_permissions.DistributorPermission]


    def get(self, request, *args, **kwargs):
        salesmen = Salesman.objects.filter(user__mobile__icontains=request.GET.get("mobile", ""))
        serializer = SalesmanSerializer(salesmen, many=True)
        return Response(serializer.data)

class InventoryTransferView(APIView):

    permission_clasess = [permissions.IsAuthenticated, local_permissions.DistributorPermission]

    def post(self, request, *args, **kwargs):
        serializer = SalesmanTransferSerializer(data=request.data, context={ "user": request.user })
        if serializer.is_valid():
            serializer.save()
            return Response(createMessage("Inventory Transferred successfully", 200), 200)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return Inventory.objects.all()


class SalesmanAddView(APIView):

    permission_classes = [permissions.IsAuthenticated, local_permissions.DistributorPermission]

    def post(self, request, *args, **kwargs):
        serializer = SalesmanAddSerializer(data=request.data, context={
            "user": request.user
        })
        if serializer.is_valid():
            serializer.save()
            return Response(createMessage("Salesman added succesfully", 200))
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return Salesman.objects.all()


class RetailerAddView(APIView):

    permission_classes = [permissions.IsAuthenticated, local_permissions.DistributorPermission]

    def post(self, request, *args, **kwargs):
        serializer = RetailerAddSerializer(data=request.data, context={
            "user": request.user
        })
        if serializer.is_valid():
            serializer.save()
            return Response(createMessage("Retailer added succesfully", 200))
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return Retailer.objects.all()

class RetailerDeleteView(APIView):

    permission_classes = [permissions.IsAuthenticated, local_permissions.DistributorPermission]

    def post(self, request, *args, **kwargs):
        serializer = RetailerDeleteSerializer(data=request.data, context={
            "user": request.user
        })
        if serializer.is_valid():
            serializer.save()
            return Response(createMessage("Retailer removed succesfully", 200))
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return Retailer.objects.all()

class SalesmanRemoveView(APIView):

    permission_classes = [permissions.IsAuthenticated, local_permissions.DistributorPermission]

    def post(self, request, *args, **kwargs):
        serializer = SalesmanDeleteSerializer(data=request.data, context={
            "user": request.user
        })
        if serializer.is_valid():
            serializer.save()
            return Response(createMessage("Salesman removed succesfully", 200))
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return Salesman.objects.all()

class GetInvoicesView(APIView):

    permission_classes = [permissions.IsAuthenticated, local_permissions.DistributorPermission]

    def get(self, request, **args):
        invoices = Invoice.objects.filter(distributor__user=request.user).values('retailer__name', 'salesman__user__first_name', 'uid', 'total_amount', 'created_at')
        return Response(invoices)
        

    def get_queryset(self):
        return Invoice.objects.all()


class InvoiceInfoView(APIView):

    permission_classes = [permissions.IsAuthenticated, local_permissions.DistributorPermission, local_permissions.SalesmanPermission]

    def get(self, request, invoice, *args):
        try:
            invoice = Invoice.objects.get(uid=invoice)
            resp = {
                "info": {
                    "uid": invoice.uid,
                    "retailer": invoice.retailer.name,
                    "balance": invoice.balance,
                    "total": invoice.total_amount,
                    "deadline": invoice.deadline,
                    "salesman": invoice.salesman.user.first_name,
                    "created_at": invoice.created_at
                },
                "sales": [],
                "transactions": []
            }
            amount = 0
            for sale in invoice.sales.all():
                resp["sales"].append({
                    "name": sale.product.name,
                    "quantity": sale.quantity,
                    "amount": sale.amount,
                    "price": sale.product.base_price
                })
                amount += sale.taxable_value
            balance_sheet = BalanceSheet.objects.filter(invoice=invoice).order_by('-created_at').values()
            resp["transactions"] = balance_sheet
            return Response(resp)
        except Invoice.DoesNotExist:
            return Response(createMessage("Requested entity does not exist", 404), status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        return super().get_queryset()
    

class AnalyticsView(APIView):

    permission_classes = [permissions.IsAuthenticated, local_permissions.DistributorPermission]

    def get(self, request):
        today = localtime()
        month_start = today.replace(day=1, second=0, minute=0, hour=0, microsecond=0)
        prev_month_end = (today.replace(day=1, second=59, minute=59, hour=23) - timedelta(days=1))
        prev_month_start = prev_month_end.replace(day=1, second=0, minute=0, hour=0)
        current_sales = Invoice.objects.filter(distributor__user=request.user, created_at__gte=month_start, created_at__lte=today).aggregate(sales=Sum('total_amount'))
        previous_sales = Invoice.objects.filter(distributor__user=request.user, created_at__gte=prev_month_start, created_at__lte=prev_month_end).aggregate(sales=Sum('total_amount'))
        if previous_sales["sales"] is None:
            previous_sales["sales"] = 0
        return Response({
            "status": (current_sales["sales"] - previous_sales["sales"]) * 100 / previous_sales["sales"] if previous_sales["sales"] else current_sales["sales"],
            "total": current_sales["sales"]
        })

    def get_queryset(self):
        return super().get_queryset()


class SalesmanListView(APIView):

    permission_classes = [permissions.IsAuthenticated, local_permissions.DistributorPermission]

    def get(self, request):
        return Response(Salesman.objects.filter(distributor__user=request.user).values('user__first_name', 'user__mobile'))

    def get_queryset(self):
        return super().get_queryset()


class RetailersListView(APIView):

    permission_classes = [permissions.IsAuthenticated, local_permissions.DistributorPermission]

    def get(self, request):
        return Response(Retailer.objects.filter(distributors__user=request.user).values('name', 'address', mobile=F('user__mobile')))

    def get_queryset(self):
        return super().get_queryset()


class TransactionsView(APIView):

    permission_classes = [permissions.IsAuthenticated, local_permissions.DistributorPermission]

    def get(self, request, *args, **kwargs):
        transactions = BalanceSheet.objects.filter(distributor__user=request.user).order_by('-created_at').values()
        return Response(transactions)

    def get_queryset(self):
        return super().get_queryset()

    
class SingleTransactionView(APIView):

    permission_classes = [permissions.IsAuthenticated, local_permissions.DistributorPermission]

    def get(self, request, transact_id, *args, **kwargs):
        transactions = BalanceSheet.objects.filter(pk=transact_id, distributor__user=request.user).values('id', 'invoice__uid', 'opening_balance', 'amount', 'remaining_balance', 'closing_balance', 'is_credit', 'payment_mode__mode__name', 'payment_mode__mode__provider', 'payment_id', 'created_by__user__first_name', 'created_by__user__last_name', 'distributor__name', 'created_at')
        try:
            return Response(transactions[0])
        except IndexError:
            return Response(createMessage("Requested entity does not exist", 404), status=404)

    def get_queryset(self):
        return super().get_queryset()

class RetailerView(APIView):

    permission_classes = [permissions.IsAuthenticated, local_permissions.DistributorPermission]

    def get(self, request, retailer):
        curr_retailer = Retailer.objects.filter(pk=retailer, distributors__user=request.user).values()
        try:
            balance = Balance.objects.get(retailer__pk=retailer)
            invoices = Invoice.objects.filter(retailer__pk=retailer, distributor__user=request.user).order_by('-created_at').values('total_amount', 'uid', 'created_at', salesman_name=F('salesman__user__first_name'))
            transactions = BalanceSheet.objects.filter(retailer__pk=retailer, distributor__user=request.user).order_by('-created_at').values('amount', 'is_credit', 'payment_mode', 'id', 'created_at', payment_image=F('payment_mode__mode__provider'), salesman=F('created_by__user__first_name'))
            return Response({
                "retailer": curr_retailer[0],
                "balance": balance.closing_balance,
                "invoices": invoices,
                "transactions": transactions
            })
        except Balance.DoesNotExist:
            return Response(createMessage("Bad request", 400), status=400)

    
    def get_queryset(self):
        return super().get_queryset()
    

class NotifyInvoice(APIView):

    permission_classes = [permissions.IsAuthenticated, local_permissions.DistributorPermission]

    def post(self, request, **args):
        current_time = now()
        today_date = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
        notification = Notifications.objects.filter(created_at__gte=today_date, type='I', retailer__pk=request.data["retailer"], distributor__user=request.user)
        if len(notification) == 0:
            try:
                curr_distributor = Distributor.objects.get(user=request.user)
                retailer = Retailer.objects.get(pk=request.data["retailer"])
                curr_invoice = Invoice.objects.get(uid=request.data["invoice"])
                message = 'Hi, {}. \nYou have a pending payment of Rs {:.2f}/- on Invoice No. {} created at {}. Last date to pay is {}.\nRegards,\n{}'.format(retailer.name, curr_invoice.balance, curr_invoice.pk, curr_invoice.created_at.strftime('%d %B %Y') ,curr_invoice.deadline.strftime('%d %B %Y'), curr_distributor.name)
                new_notification = Notifications(retailer=retailer, entity=curr_invoice.pk, distributor=curr_distributor, message=message, type='I')
                send_message(message, retailer.user.mobile)
                new_notification.save()
                return Response(createMessage("Message has been sent", 200), status=200)
            except (Retailer.DoesNotExist, Invoice.DoesNotExist):
                return Response(createMessage("Bad request", 400), status=400)
        else:
            return Response(createMessage("Message has already been sent", 200), status=200)

    def get_queryset(self):
        return super().get_queryset()

class DeleteCategoryView(APIView):


    def post(self, request):
        try:
            category = Type.objects.get(pk=request.data["category"])
            category.is_deleted = True
            category.updated_at = now()
            category.save()
            return Response(createMessage("{} deleted successfully".format(category.name), 400), status=400)
        except Type.DoesNotExist:
            return Response(createMessage("Bad request", 400), status=400)

    def get_queryset(self):
        return super().get_queryset()

class DeleteInventoryView(APIView):


    def post(self, request):
        try:
            product = Product.objects.get(pk=request.data["product"])
            product.is_deleted = True
            product.updated_at = now()
            product.save()
            return Response(createMessage("{} deleted successfully".format(category.name), 400), status=400)
        except Product.DoesNotExist:
            return Response(createMessage("Bad request", 400), status=400)

    def get_queryset(self):
        return super().get_queryset()


class PaymentModeListView(APIView):

    def get(self, request):
        modes = PaymentMode.objects.all()
        serializer = PaymentModeSerializer(modes, many=True)
        return Response(serializer.data) 

    def get_queryset(self):
        modes = PaymentMode.objects.all()
        return modes


class PaymentMethodListView(APIView):

    def post(self, request):
        methods = PaymentMethod.objects.filter(distributor=request.data["distributor"], is_deleted=False)
        serializer = PaymentMethodListSerializer(methods, many=True)
        return Response(serializer.data) 

    def get_queryset(self):
        modes = PaymentMethod.objects.all()
        return modes


class PaymentMethodCreationView(APIView):

    def post(self, request):
        serializer = PaymentMethodSerializer(data=request.data, context={
            "user": request.user
        })
        if serializer.is_valid():
            serializer.save()
            return Response(createMessage("Payment method created sucessfully", 200), 200)
        else:
            return Response(serializer.errors, 400)

    def get_queryset(self):
        modes = PaymentMethod.objects.all()
        return modes


class DeletePaymentView(APIView):


    def post(self, request):
        try:
            method = PaymentMethod.objects.get(pk=request.data["distributor"])
            method.is_deleted = True
            method.updated_at = now()
            method.save()
            return Response(createMessage("{} deleted successfully".format(method.mode.name), 400), status=400)
        except Product.DoesNotExist:
            return Response(createMessage("Bad request", 400), status=400)


    def get_queryset(self):
        modes = PaymentMethod.objects.all()
        return modes