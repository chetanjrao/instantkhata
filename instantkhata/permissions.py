from accounts.models import User
from rest_framework.permissions import BasePermission

class DistributorPermission(BasePermission):

    def has_permission(self, request, view):
        user = User.objects.get(pk=request.user.pk)
        return user.role == 3 or user.role == 2 or user.role == 1


class AdministratorPermission(BasePermission):

    def has_permission(self, request, view):
        user = User.objects.get(pk=request.user.pk)
        return user.role == 1


class RetailerPermission(BasePermission):

    def has_permission(self, request, view):
        user = User.objects.get(pk=request.user.pk)
        return user.role == 1 or user.role == 2 or user.role == 4


class SalesmanPermission(BasePermission):

    def has_permission(self, request, view):
        user = User.objects.get(pk=request.user.pk)
        return user.role == 1 or user.role == 2 or user.role == 5

class SupportStaffPermission(BasePermission):

    def has_permission(self, request, view):
        user = User.objects.get(pk=request.user.pk)
        return user.role == 1 or user.role == 2