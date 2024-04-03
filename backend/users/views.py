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

    def _set_authentication_cookies(self, response: Response):
        data = response.data
        access = data.get("access")
        refresh = data.get("refresh")
        response.data = None

        response.set_cookie(
            "access_token",
            access,
            httponly=True,
        )
        response.set_cookie(
            "refresh_token",
            refresh,
            httponly=True,
        )
        return response

    def post(self, request, format=None):
        response = super().post(request)
        self._set_authentication_cookies(response)
        return response


class UserView(viewsets.GenericViewSet):
    def retrieve_self(self, request, format=None):
        user = request.user
        if not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user = User.objects.get(id=user.id)
        return Response(UserSerializer(user).data)
