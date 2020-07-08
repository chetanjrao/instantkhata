from django.urls import path
from .views import SalesCreationView, InvoiceCreationView, invoice_view

urlpatterns = [
    path('sales/create/', InvoiceCreationView.as_view(), name="sales_creation"),
    path('sales/invoice/<str:invoice>', invoice_view, name="invoice")
]