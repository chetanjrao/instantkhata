from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from .serializers import DistributorSerializer, InventorySerializer, BaseInventorySerializer, TypeCreationSerializer, SalesmanSerializer, SalesmanTransferSerializer, SalesmanAddSerializer, SalesmanDeleteSerializer
from rest_framework.response import Response
from instantkhata import permissions as local_permissions
from instantkhata.utils import createMessage
from rest_framework import status
from .models import Product, Type, Distributor
from salesman.models import Salesman, Inventory

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
            return Response(createMessage("Inventory Transferred successfully", 200))
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