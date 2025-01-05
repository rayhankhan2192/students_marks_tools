from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import Account, OTP
from .serializers import RegistrationSerializer, OTPVerificationSerializers

class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data = request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            otp_code = get_random_string(length=6, allowed_chars='1234567890')
            OTP.objects.create(user = user, otp_code = otp_code)
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp_code}. It will expire in 90 seconds.',
                [user.email],
                fail_silently=False,
            )
            return Response({'message': 'User registered successfully. OTP sent to email.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OTPVerificationView(APIView):
    def post(self, request):
        serializer = OTPVerificationSerializers(data=request.data)
        if serializer.is_valid():
            user = Account.objects.get(email=serializer.validated_data['email'])
            user.is_active = True
            user.save()
            return Response({'message': 'OTP verified successfully. User activated.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)