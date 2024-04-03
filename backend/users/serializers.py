from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as DefaultTokenObtainPairSerializer,
)

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "full_name", "email")


class EmailTokenObtainPairSerializer(DefaultTokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD
