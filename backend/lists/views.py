from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import User

from .models import Compilation
from .serializers import CompilationCreateSerializer, CompilationSerializer


class CompilationView(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Compilation.objects.all()
    permission_classes = [IsAuthenticated]
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
