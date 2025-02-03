from django.urls import path
from . import views

from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('verify-otp/', views.OTPVerificationView.as_view(), name='verify-otp'),
    path('resend_otp/', views.ResendOTPView.as_view(), name='resend_otp'),
    path('login/', TokenObtainPairView.as_view(), name="login"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]