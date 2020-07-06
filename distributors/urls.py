from django.urls import path, re_path
from django.conf.urls import url
from .views import DistributorRegistration, InventoryCreationView, InventoryListView, TypeCreationView, SalesmanListSerializer, InventoryTransferView, SalesmanAddView, SalesmanRemoveView

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
    path('salesman/remove/', SalesmanRemoveView.as_view(), name="remove_salesman")

]