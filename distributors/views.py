from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView
from .serializers import DistributorSerializer, InventorySerializer
from rest_framework.response import Response

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

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.data["distributor"] = request.user.pk
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

# class InventoryEditView(APIView):

#     per