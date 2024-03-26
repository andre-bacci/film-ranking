from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny

from .models import Compilation
from .serializers import CompilationSerializer


class CompilationView(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Compilation.objects.all()
    serializer_class = CompilationSerializer
    permission_classes = [AllowAny]
    search_fiels = ["title"]
