from django.shortcuts import render
from .serializers import SalesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from ledger.models import Sale
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