from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as DefaultTokenObtainPairSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import UserSerializer


class Login(TokenObtainPairView):
    serializer_class = DefaultTokenObtainPairSerializer


class UserView(viewsets.GenericViewSet):
    def retrieve_self(self, request, format=None):
        user = request.user
        if not user or not user.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user = User.objects.get(id=user.id)
        return Response(UserSerializer(user).data)
