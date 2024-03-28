from django.shortcuts import render
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as DefaultTokenObtainPairSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.


class Login(TokenObtainPairView):
    serializer_class = DefaultTokenObtainPairSerializer
