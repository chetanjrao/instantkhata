from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt
from .views import SalesCreationView, InvoiceCreationView, invoice_view, InvoiceEditView, SalesmanAnalyticsView, TransactionList, RetailersListView, InventoryListView, InvoiceListView, TransactionView, Distributors, AllTransactionList, PaymentListView, TypesView

urlpatterns = [
    path('sales/create/', InvoiceCreationView.as_view(), name="sales_creation"),
    path('sales/invoice/edit/', InvoiceEditView.as_view(), name="update_invoice"),
    path('sales/invoice/<str:invoice>/', invoice_view, name="sales_invoice"),
    path('analytics/', SalesmanAnalyticsView.as_view(), name="sales_analytics"),
    path('transactions/', TransactionList.as_view(), name="sales_transactions"),
    path('transactions/all/', AllTransactionList.as_view(), name="sales_all_transactions"),
    path('transactions/<int:t_id>/', TransactionView.as_view(), name="sales_transactions_info"),
    re_path(r'^retailers/$', RetailersListView.as_view(), name="sales_reatilers"),
    path('inventory/', InventoryListView.as_view(), name="sales_inventory"),
    path('invoices/', InvoiceListView.as_view(), name="sales_invoice_list"),
    path('payments/', PaymentListView.as_view(), name="sales_payments_list"),
    path('categories/', TypesView.as_view(), name='types'),
    path('distributors/', Distributors.as_view(), name="sales_distributors")
]