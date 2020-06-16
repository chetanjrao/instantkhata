from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.http import JsonResponse
from .models import User
from .serializers import UserSerializer, OTPSerializer

# Create your views here.
@csrf_exempt
class UserManager(APIView):
    
    def post(self, *args, **kwargs):
        pass

class AuthManager(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)