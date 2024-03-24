from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib import auth
from .serializers import LoginSerializer, RegisterSerializer

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



        