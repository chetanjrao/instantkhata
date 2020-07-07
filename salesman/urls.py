from django.urls import path
from .views import SalesCreationView, InvoiceCreationView

urlpatterns = [
    path('sales/create/', InvoiceCreationView.as_view(), name="sales_creation")
]