from rest_framework import serializers
from .models import Account, OTP
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'first_name',
            'last_name',
            'email',
            'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        user = Account.objects.create_user(**validated_data)
        return user

class OTPVerificationSerializers(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length = 6)
    
    def validate(self, data):
        email = data.get('email')
        otp_code = data.get('otp_code')
        
        try:
            user = Account.objects.get(email = email)
        except Account.DoesNotExist:
            raise serializers.ValidationError('User with this email does not exist.')
        
        try:
            otp = OTP.objects.filter(user = user).latest('created_at')
            if otp.otp_code != otp_code:
                raise serializers.ValidationError('Invalid OTP.')
            if otp.is_expired():
                raise serializers.ValidationError('OTP has expired.')
        except OTP.DoesNotExist:
            raise serializers.ValidationError('No OTP found for this user.')
        
        return data
    
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    # def validate(self, attrs):
    #     email = attrs.get('email')
    #     password = attrs.get('password')

    #     user = authenticate(email=email, password=password)
    #     if user is None:
    #         raise serializers.ValidationError("Invalid credentials")

    #     attrs['user'] = user
    #     return attrs
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'email', 'first_name', 'last_name', 'is_admin', 'is_staff']