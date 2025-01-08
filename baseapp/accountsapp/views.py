from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import Account, OTP
from .serializers import RegistrationSerializer, OTPVerificationSerializers
from django.db import transaction
from django.utils.timezone import now


class RegistrationView(APIView):
    # def post(self, request):
    #     serializer = RegistrationSerializer(data = request.data)
        
    #     if serializer.is_valid():
    #         user = serializer.save()
    #         otp_code = get_random_string(length=6, allowed_chars='1234567890')
    #         OTP.objects.create(user = user, otp_code = otp_code)
    #         send_mail(
    #             'Your OTP Code',
    #             f'Your OTP code is {otp_code}. It will expire in 90 seconds.',
    #             '',
    #             [user.email],
    #             fail_silently=False,
    #         )
    #         return Response({'message': 'User registered successfully. OTP sent to email.'}, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            
            try:
                with transaction.atomic():  # Start a transaction
                    user = serializer.save()
                    # Generate OTP
                    otp_code = get_random_string(length=6, allowed_chars='1234567890')
                    OTP.objects.create(user=user, otp_code=otp_code)
                    # Send email
                    send_mail(
                        'Your OTP Code',
                        f'Your OTP code is {otp_code}. It will expire in 90 seconds.',
                        '',
                        [user.email],
                        fail_silently=False,
                    )
                    # If email is successfully sent, commit the transaction
                    return Response({'message': 'User registered successfully. OTP sent to email.'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                # Roll back transaction if email sending fails or any error occurs
                return Response({'error': 'Registration failed. Please try again later.', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)
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
    
class ResendOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)
        user = Account.objects.filter(email = email).first()
        if not user:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        if user.is_active:
            return Response({'error': 'User is already active. Please log in.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                otp_code = get_random_string(length=6, allowed_chars='1234567890')
                OTP.objects.create(user=user, otp_code=otp_code)
                
                send_mail(
                    'Your New OTP Code',
                    f'Your New OTP code is {otp_code}. It will expire in 90 seconds.',
                    '',
                    [email],
                    fail_silently=False,
                )
                return Response({'message': 'OTP resent successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Failed to resend OTP.', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)