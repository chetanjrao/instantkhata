from django.urls import path
from .views import SalesCreationView

urlpatterns = [
    path('sales/create/', SalesCreationView.as_view(), name="sales_creation")
]