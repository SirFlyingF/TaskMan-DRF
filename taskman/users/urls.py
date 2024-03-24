from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView, RegisterView, LogoutView

urlpatterns = [
    path('api/token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    # password reset request takes username, and sends email to registered email
    # password reset verify, email contains link to this url, returns next : link to redirect url
    # password reset takes two passwords, sets it to user , returns success 
]
