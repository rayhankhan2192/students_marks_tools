from django.urls import path
from .views import RegistrationView, OTPVerificationView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('verify-otp/', OTPVerificationView.as_view(), name='verify-otp'),
]