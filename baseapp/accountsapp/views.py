from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import Account, OTP
from .serializers import RegistrationSerializer, OTPVerificationSerializers, LoginSerializer, UserSerializer
from django.db import transaction
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import login

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
        serializer = RegistrationSerializer(data=request.data, context={'request': request})
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
                    return Response({'message': 'An OTP has been sent to email. Please verified!'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                # Roll back transaction if email sending fails or any error occurs
                return Response({'message': 'Registration failed. Please try again later.', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class OTPVerificationView(APIView):
    def post(self, request):
        serializer = OTPVerificationSerializers(data=request.data)
        if serializer.is_valid():
            user = Account.objects.get(email=serializer.validated_data['email'])
            user.is_active = True
            user.save()
            otp_instance = OTP.objects.filter(user = user).first()
            otp_instance.delete()
            return Response({'message': 'OTP verified successfully. User activated.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ResendOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'message': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)
        user = Account.objects.filter(email = email).first()
        if not user:
            return Response({'message': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        if user.is_active:
            return Response({'message': 'User is already active. Please log in.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                # otp_code = get_random_string(length=6, allowed_chars='1234567890')
                # OTP.objects.create(user=user, otp_code=otp_code)
                otp_instance, created = OTP.objects.get_or_create(user=user)
                
                # if not created:  # If the OTP already exists
                #     elapsed_time = (now() - otp_instance.created_at).total_seconds()
                #     if elapsed_time < 90:
                #         return Response({'error': 'OTP is still valid. Please wait for it to expire.'}, status=status.HTTP_400_BAD_REQUEST)

                # Update the existing OTP instance with a new OTP code and time
                otp_code = get_random_string(length=6, allowed_chars='1234567890')
                while otp_instance.otp_code == otp_code:
                    otp_code = get_random_string(length=6, allowed_chars='1234567890')
                otp_instance.otp_code = otp_code
                otp_instance.created_at = now()
                otp_instance.save()
                send_mail(
                    'Your New OTP Code',
                    f'Your New OTP code is {otp_code}. It will expire in 90 seconds.',
                    '',
                    [email],
                    fail_silently=False,
                )
                return Response({'message': 'OTP resent successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Failed to resend OTP.', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # You can return the token here if you're using token-based authentication
            # Example: Use Django REST Framework's Token Authentication
            return Response({
                'message': 'Login successful',
                'email': user.email,
                'full_name': user.full_name(),
                'is_admin': user.is_admin,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)