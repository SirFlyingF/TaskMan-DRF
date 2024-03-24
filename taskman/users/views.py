from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_bytes
from django.core.mail import EmailMessage
from taskman import settings
from .serializers import LoginSerializer, RegisterSerializer, PasswordResetCompleteSerializer, PasswordResetRequestSerializer

# Create your views here.


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = User.objects.filter(username=username)
        if not user:
            return Response({"msg":"User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        user = auth.authenticate(request, username=username, password=password)
        if not user:
            return Response({"msg":"Invalid email or password"}, status=status.HTTP_200_OK)
        
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token),}, status=status.HTTP_200_OK)


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        username = data.get('username')

        if User.objects.filter(username=username).exists():
            return Response({"msg":"User already exists"}, status=status.HTTP_409_CONFLICT)
        
        if not data.get('password1') == data.get('password2'):
            return Response({'msg' : "Password1 and Password2 did not match"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create(username=username, email=data.get('email'))
        user.set_password(data.get('password1'))
        user.save()

        return Response({'msg' : "Success!"}, status=status.HTTP_201_CREATED)
                   

class LogoutView(APIView):
    # Not sure why but need to override auth classes to prevent Unauthenticated error
    # Perhaps because settings have Authentication classes defined but shouldnt that be a
    # permission_classes = [isAuthenticated] ?
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        refresh_token = request.headers.get('Authorization', '').split(' ')[1]

        if not refresh_token:
            return Response({"msg": "No token in Authorization header"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            RefreshToken(refresh_token).blacklist()
        except Exception as e:
            print(str(e))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"msg" : "Success!"}, status=status.HTTP_200_OK)
    

class PasswordResetRequestView(APIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        username = serializer.validated_data.get('username')
        if not User.objects.filter(username=username).exists():
            return Response({"msg":"User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        uzr = User.objects.filter(username=username)
        if not uzr.email:
            # This should not be hit if email is a required field.
            # Ideally email should be set to AUTH_USERNAME_FIELD
            return Response({"msg" : "No registered email for the user"}, status=status.HTTP_404_NOT_FOUND)
        
        uidb64 = urlsafe_base64_encode(smart_bytes(uzr.id))
        token = PasswordResetTokenGenerator().make_token(uzr)

        current_site = get_current_site(request=request).domain
        relativeLink = reverse('password-reset-verify', kwargs={'uidb64': uidb64, 'token': token})
        
        absurl = 'http://'+current_site+relativeLink

        frm = settings.EMAIL_HOST_USER
        to = uzr.email
        subject ='Reset your passsword'
        message =   'Hello,'                                  +'\n'+\
                    'Use link below to reset your password.'  +'\n'+\
                        absurl                                   +'\n'+\
                                                            +'\n'+\
                    'Regards'

        try:   
            email = EmailMessage(subject, message, frm, to)
            email.send()
        except Exception as e:
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"msg" : "Success!"}, status=status.HTTP_200_OK)
    

class PasswordResetVerifyView(APIView):
    def get(self, request):
        pass