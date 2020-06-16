from .models import User, OTP
from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.serializers import ValidationError
from random import randint
from django.utils import timezone
import datetime

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'mobile', 'last_login']

    def create(self, validated_data):
        user = get_user_model().objects.create(**validated_data)
        password = User.objects.make_random_password(length=16)
        user.set_password(password)
        user.save()
        return user

class OTPSerializer(serializers.Serializer):
    user = serializers.CharField(max_length=10)

    def validate_user(self, user):
        try:
            user = User.objects.get(mobile=user)
        except User.DoesNotExist:
            raise ValidationError("Requested mobile is not associated with any user")
        return user

    def create(self, validated_data):
        otp = randint(1000, 9999)
        expiry = timezone.now() + datetime.timedelta(minutes=10)
        otp_document = OTP.objects.create(user=validated_data["user"], otp=otp, expires_at=expiry)
        otp_document.save()
        return otp_document


    def update(self, validated_data):
        pass
        
class OTPValidator(serializers.Serializer):
    user = serializers.CharField(max_length=10)
    otp = serializers.CharField(max_length=4)

    def validate_user(self, user):
        try:
            user = User.objects.get(mobile=user)
        except User.DoesNotExist:
            raise ValidationError("Requested mobile is not associated with any user")
        return user
    
    def validate_otp(self, user, otp):
        try:
            otp_check = OTP.objects.get(user=user, otp=otp)
            if otp_check.is_used or timezone.now() < otp_check.expires_at:
                raise ValidationError("OTP has been expired")
            else:
                return otp_check
        except:
            raise ValidationError("Invalid OTP")