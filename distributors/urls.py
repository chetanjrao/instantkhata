from django.urls import path, re_path
from django.conf.urls import url
from .views import (DistributorRegistration, InventoryCreationView, 
InventoryListView, TypeCreationView, SalesmanListSerializer, 
InventoryTransferView, SalesmanAddView, 
SalesmanRemoveView, GetInvoicesView, 
InvoiceInfoView, AnalyticsView, SalesmanListView,
RetailersListView, RetailerAddView, RetailerDeleteView,
TransactionsView, SingleTransactionView, RetailerView
)

urlpatterns = [
    path('register/', DistributorRegistration.as_view(), name='distributor_registration'),
    path('inventory/', InventoryListView.as_view(), name="inventory"),
    path('inventory/add/', InventoryCreationView.as_view(), name='distributor_add_inventory'),
    path('inventory/<int:pk>/add/', InventoryCreationView.as_view(), name='distributor_add_inventory'),
    path('inventory/types/', TypeCreationView.as_view(), name="get_types"),
    path('inventory/types/add/', TypeCreationView.as_view(), name="add_types"),
    re_path(r'^search/salesman/$', SalesmanListSerializer.as_view(), name="salesman_list"),
    path('inventory/transfer/', InventoryTransferView.as_view(), name="inventory_transfer"),
    path('salesman/add/', SalesmanAddView.as_view(), name="add_salesman"),
    path('salesman/remove/', SalesmanRemoveView.as_view(), name="remove_salesman"),
    path('invoices/', GetInvoicesView.as_view(), name='distributors_invoices'),
    path('invoices/info/<str:invoice>/', InvoiceInfoView.as_view(), name="distributors_invoice_info"),
    path('analytics/', AnalyticsView.as_view(), name='analytics_view'),
    path('salesman/', SalesmanListView.as_view(), name='distributors_salesman'),
    path('retailers/', RetailersListView.as_view(), name='distributors_retailers'),
    path('retailers/<int:retailer>/', RetailerView.as_view(), name='distributors_retailers_info'),
    path('retailers/add/', RetailerAddView.as_view(), name="add_retailer"),
    path('retailers/remove/', RetailerDeleteView.as_view(), name="remove_retailer"),
    path('transactions/', TransactionsView.as_view(), name='transactions'),
    path('transactions/<int:transact_id>/', SingleTransactionView.as_view(), name='single_transaction')
]