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
from django.utils.encoding import smart_bytes, smart_str
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from taskman import settings
from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    LogoutSerializer
)

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
            return Response({"msg":"Invalid username or password"}, status=status.HTTP_200_OK)
        
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
    serializer_class = LogoutSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response({"msg": "No token in Authorization header"}, status=status.HTTP_400_BAD_REQUEST)
        
        refresh_token = serializer.validated_data.get('refresh')
        try:
            RefreshToken(refresh_token).blacklist()
        except Exception as e:
            print(str(e))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"msg" : "Success!"}, status=status.HTTP_200_OK)
    

class PasswordResetRequestView(APIView):
    serializer_class = PasswordResetRequestSerializer
    authentication_classes = [] # Override to not expect an access token

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        username = serializer.validated_data.get('username')
        if not User.objects.filter(username=username).exists():
            return Response({"msg":"User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        uzr = User.objects.filter(username=username).first()
        if not uzr.email:
            # This should not be hit if email is a required field.
            # Ideally email should be set to AUTH_USERNAME_FIELD
            return Response({"msg" : "No registered email for the user"}, status=status.HTTP_404_NOT_FOUND)
        
        uidb64 = urlsafe_base64_encode(smart_bytes(uzr.id))
        token = PasswordResetTokenGenerator().make_token(uzr)

        current_site = get_current_site(request=request).domain
        relative_link = reverse('password-reset-verify', kwargs={'uidb64': uidb64, 'token': token})
        
        absurl = 'http://'+current_site+relative_link

        frm =      settings.EMAIL_HOST_USER
        to =       [uzr.email]
        subject = 'Reset your passsword'
        message = 'Hello, ' + uzr.username                  +'\n'+\
                                                             '\n'+\
                  'Use link below to reset your password.'  +'\n'+\
                   absurl                                   +'\n'+\
                                                             '\n'+\
                  'Regards'

        try:   
            email = EmailMessage(subject, message, frm, to)
            # email.send()
        except Exception as e:
            return Response({"msg" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"msg" : "Success!", "uidb64":uidb64, "token":token}, status=status.HTTP_200_OK)
    

class PasswordResetVerifyView(APIView):
    authentication_classes = []

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))

            uzr = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(uzr, token):
                raise KeyError  # Will be caught with a relevant message

            # Redirect tp FrontEnd_PasswordReset_URL for React/Angular front end
            # fe_pr_url = settings.FRONTEND_URL + f'/password-reset-confirm/?token={token}&uidb64={uidb64}'
            # return redirect(fe_pr_url)
            return Response({"msg" : "success"}, status=status.HTTP_200_OK)
        
        except KeyError as ke:
            return Response({'msg' : "This is not the link you are looking for"}, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist as e_404:
            return Response({"msg":"User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except AssertionError:
            return Response({"msg":"User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        

class PasswordResetConfirmView(APIView):
    authentication_classes = []

    serializer_class = PasswordResetConfirmSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        password1 = serializer.validated_data.get('password1')
        password2 = serializer.validated_data.get('password2')
        token = request.GET.get('token')
        id = smart_str(urlsafe_base64_decode(request.GET.get('uidb64')))

        try:
            uzr = User.objects.get(id=id)
            if not uzr:
                return Response({"msg":"User does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
            if not PasswordResetTokenGenerator().check_token(uzr, token):
                return Response({'msg' : "This is not the link you are looking for"}, status=status.HTTP_403_FORBIDDEN)

            if not password1 == password2:
                return Response({'msg' : "Password1 and Password2 did not match"}, status=status.HTTP_400_BAD_REQUEST)
        
            uzr.set_password(password1)
            uzr.save()
        except Exception:
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'msg' : "Success!"}, status=status.HTTP_201_CREATED)