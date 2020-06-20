from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView
from .serializers import DistributorSerializer, InventorySerializer
from rest_framework.response import Response
from instantkhata import permissions as local_permissions
from instantkhata.utils import createMessage
from rest_framework import status

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
        pass

class InventoryCreationView(APIView):

    permission_classes = [permissions.IsAuthenticated, local_permissions.DistributorPermission]

    def post(self, request, *args, **kwargs):
        request.data["distributor"] = request.user.pk
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(createMessage("Item added successfully", status.HTTP_200_OK))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class InventoryEditView(APIView):

#     per