from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import SalesCreationView, InvoiceCreationView, invoice_view, InvoiceEditView

urlpatterns = [
    path('sales/create/', InvoiceCreationView.as_view(), name="sales_creation"),
    path('sales/invoice/edit/', InvoiceEditView.as_view(), name="update_invoice"),
    path('sales/invoice/<str:invoice>/', invoice_view, name="invoice")
]