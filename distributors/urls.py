from django.urls import path
from .views import DistributorRegistration, InventoryCreationView

urlpatterns = [
    path('register/', DistributorRegistration.as_view(), name='distributor_registration'),
    path('inventory/add/', InventoryCreationView.as_view(), name='distributor_add_inventory'),
    # path('inventory/view/<int:id>'),
    # path('inventory/edit/<int:id>'),
    # path('inventory/transfer/'),
    # path('inventory/edit/<int:id>/add')
]