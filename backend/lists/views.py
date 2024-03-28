from django.db import transaction
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from users.models import User

from .models import Compilation, List
from .serializers import (
    CompilationCreateSerializer,
    CompilationSerializer,
    ListCreateSerializer,
    ListSerializer,
)


class CompilationView(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Compilation.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ["title"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CompilationSerializer
        if self.action == "create":
            return CompilationCreateSerializer

    def create(self, request, format=None):
        user: User = request.user
        compilation_serializer = CompilationCreateSerializer(data=request.data)
        compilation_serializer.is_valid(raise_exception=True)
        compilation: Compilation = compilation_serializer.save()
        compilation.owners.add(user)
        return Response(CompilationSerializer(compilation).data)


class ListView(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = List.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ["title"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ListSerializer
        if self.action == "create":
            return ListCreateSerializer

    @transaction.atomic
    def create(self, request, compilation_id, format=None):
        user: User = request.user
        if not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        list_serializer = ListCreateSerializer(data=request.data)
        list_serializer.is_valid(raise_exception=True)
        list: List = list_serializer.create(
            validated_data=list_serializer.validated_data,
            compilation_id=compilation_id,
            author_id=user.id,
        )
        return Response(ListSerializer(list).data)
