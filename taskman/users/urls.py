from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView, RegisterView, LogoutView, PasswordResetRequestView, PasswordResetVerifyView, PasswordResetConfirmView

urlpatterns = [
    path('api/token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/password-reset-request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('api/password-reset-verify//<uidb64>/<token>/', PasswordResetVerifyView.as_view(), name='password-reset-verify'),
    path('api/password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
