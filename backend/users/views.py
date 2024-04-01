from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as DefaultTokenObtainPairSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView


class Login(TokenObtainPairView):
    serializer_class = DefaultTokenObtainPairSerializer
