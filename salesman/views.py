from django.shortcuts import render
from .serializers import SalesSerializer, InvoiceSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ledger.models import Sale
from distributors.views import createMessage
# Create your views here.


class SalesCreationView(APIView):

    def post(self, request, *args, **kwargs):
        sales_seralizer = SalesSerializer(data=request.data, many=True)
        if sales_seralizer.is_valid():
            return Response(sales_seralizer.data)
        else:
            return Response(sales_seralizer.errors)

    def get_queryset(self):
        return Sale.objects.all()


class InvoiceCreationView(APIView):

    def post(self, request, *args, **kwargs):
        invoice_seralizer = InvoiceSerializer(data=request.data, context={
            "user": request.user
        })
        if invoice_seralizer.is_valid():
            new_invoice = invoice_seralizer.save()
            return Response(createMessage("Invoice created successfully", 200))
        else:
            return Response(invoice_seralizer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return Sale.objects.all()