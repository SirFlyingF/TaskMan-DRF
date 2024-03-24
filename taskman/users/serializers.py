from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.fields import EmailField, CharField
from django.contrib.auth.models import User
    

class LoginSerializer(Serializer):
    username = CharField()
    password = CharField(min_length=8)


class RegisterSerializer(ModelSerializer):
    email = EmailField()
    password1 = CharField(min_length=8)
    password2 = CharField(min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



