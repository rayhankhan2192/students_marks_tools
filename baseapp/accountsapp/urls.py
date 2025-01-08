from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('verify-otp/', views.OTPVerificationView.as_view(), name='verify-otp'),
    path('resend_otp/', views.ResendOTPView.as_view(), name='resend_otp'),
]