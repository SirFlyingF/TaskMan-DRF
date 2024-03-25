from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.fields import EmailField, CharField
from django.contrib.auth.models import User
    

class LoginSerializer(Serializer):
    username = CharField()
    password = CharField(min_length=8)


class RegisterSerializer(ModelSerializer):
    email = EmailField(required=True)
    username = CharField(required=True)
    password1 = CharField(min_length=8, required=True)
    password2 = CharField(min_length=8, required=True)


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PasswordResetRequestSerializer(Serializer):
    username = CharField(required=True)


class PasswordResetConfirmSerializer(Serializer):
    password1 = CharField(min_length=8)
    password2 = CharField(min_length=8)

    




