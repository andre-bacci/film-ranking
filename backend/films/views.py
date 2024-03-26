from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import AllowAny

from .models import Film
from .serializers import FilmSerializer


class FilmView(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["imdb_id", "tmdb_id", "title", "original_title", "pt_br_title"]
