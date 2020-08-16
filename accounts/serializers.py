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
        fields = ['first_name', 'last_name', 'email', 'image']
        
    def create(self, validated_data):
        user = get_user_model().objects.create(**validated_data)
        password = User.objects.make_random_password(length=16)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.image = validated_data.get("image", instance.image)
        instance.email = validated_data.get("email", instance.email)
        instance.save()
        return instance

class OTPSerializer(serializers.Serializer):
    user = serializers.CharField(max_length=10)
    role = serializers.IntegerField()

    def validate_user(self, user):
        try:
            user = User.objects.get(mobile=user, role=self.initial_data["role"])
        except User.DoesNotExist:
            raise ValidationError("Requested mobile is not associated with any user")
        return user

    def create(self, validated_data):
        otp = randint(1000, 9999)
        expiry = timezone.now() + datetime.timedelta(minutes=10)
        otp_document = OTP.objects.create(user=validated_data["user"], otp=otp, expires_at=expiry)
        otp_document.save()
        print(otp)
        return otp_document


    def update(self, instance, validated_data):
        pass
        
class OTPValidator(serializers.Serializer):
    user = serializers.CharField(max_length=10)
    otp = serializers.CharField(max_length=4)

    def validate_user(self, user):
        try:
            self._user = User.objects.get(mobile=user)
        except User.DoesNotExist:
            raise ValidationError("Requested mobile is not associated with any user")
        return user
    
    def validate_otp(self, otp):
        try:
            otp_check = OTP.objects.filter(user=self._user, otp=otp).order_by('-created_at')[0]
            if otp_check.is_used or timezone.now() > otp_check.expires_at:
                raise ValidationError("OTP has been expired")
            else:
                return otp_check
        except:
            raise ValidationError("Invalid OTP")

    def update(self, instance):
        instance.is_used = True
        instance.save()
        return instance