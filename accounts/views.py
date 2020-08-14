from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.http import JsonResponse
from .models import User, OTP
from .serializers import UserSerializer, OTPSerializer, OTPValidator

# Create your views here.
class UserManager(APIView):

    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        _jwt_client = JWTAuthentication()
        current_user:User = request.user
        return Response(current_user.get_profile())

class RegisterView(APIView):

    def post(self, request, *agrs):
        serializer = UserSerializer(data=request.data)

class AuthManager(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={
                "message": "OTP sent successfully",
                "status": 200
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

class OTPManager(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        validator = OTPValidator(data=request.data)
        if validator.is_valid():
            user = User.objects.get(mobile=validator.data["user"])
            otp = OTP.objects.filter(user=user, otp=validator.data["otp"]).order_by('-created_at')[0]
            validator.update(otp)
            try:
                refresh_token = RefreshToken.for_user(user)
                return Response({
                    "access_token": str(refresh_token.access_token),
                    "refresh_token": str(refresh_token)
                })
            except TokenError:
                return Response(data={
                    "message": "Error procrocessing your request",
                    "status": 500
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(validator.data)
        return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)


class EditProfileView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(request.user, serializer.validated_data)
            return Response({
                "message": "Profile saved successfully",
                "status": 200
            })
        else:
            return Response(serializer.errors)