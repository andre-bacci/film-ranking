from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from users.models import User

from .models import Compilation, List, Ranking
from .serializers import (
    CompilationCreateSerializer,
    CompilationSerializer,
    ListCreateSerializer,
    ListSerializer,
    RankingSerializer,
)


class CompilationView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Compilation.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ["title"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CompilationSerializer
        if self.action == "create":
            return CompilationCreateSerializer

    @transaction.atomic
    def create(self, request, format=None):
        user = request.user
        if not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user = User.objects.get(id=user.id)

        compilation_serializer = CompilationCreateSerializer(data=request.data)
        compilation_serializer.is_valid(raise_exception=True)
        compilation: Compilation = compilation_serializer.save()
        compilation.owners.add(user)

        return Response(CompilationSerializer(compilation).data)

    @transaction.atomic
    def update(self, request, pk, format=None):
        try:
            instance = Compilation.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user = User.objects.get(id=user.id)
        if user not in instance.owners.all():
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        compilation_serializer = CompilationCreateSerializer(
            instance, data=request.data
        )
        compilation_serializer.is_valid(raise_exception=True)
        compilation: Compilation = compilation_serializer.save()

        return Response(CompilationSerializer(compilation).data)

    @transaction.atomic
    def calculate_ranking(self, request, pk, format=None):
        try:
            compilation = Compilation.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        ranking = compilation.calculate_ranking()
        return Response(data=RankingSerializer(ranking).data)


class ListView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
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
    def create(self, request, format=None):
        user: User = request.user
        if not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        list_serializer = ListCreateSerializer(data=request.data)
        list_serializer.is_valid(raise_exception=True)
        if List.exists_by_user_and_compilation(
            user_id=user.id,
            compilation_id=list_serializer.validated_data.get("compilation_id"),
        ):
            return Response(
                data={"message": "A list for this user and compilation already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        list: List = list_serializer.save(author_id=user.id)

        return Response(ListSerializer(list).data)

    @transaction.atomic
    def update(self, request, pk, format=None):
        try:
            instance = List.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user: User = request.user
        if not user or instance.author_id != user.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        list_serializer = ListCreateSerializer(instance, data=request.data)
        list_serializer.is_valid(raise_exception=True)

        list: List = list_serializer.save()
        return Response(ListSerializer(list).data)


class RankingView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Ranking.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ["title"]
    serializer_class = RankingSerializer
