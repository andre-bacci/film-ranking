from django.db import transaction
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Film
from .serializers import FilmSerializer
from .services import FilmService


class FilmView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["imdb_id", "tmdb_id", "title", "original_title", "pt_br_title"]
    film_service = FilmService()

    @transaction.atomic
    def retrieve(self, request, imdb_id, format=None):
        film = self.film_service.get_film(imdb_id=imdb_id)
        serializer = FilmSerializer(film)
        return Response(serializer.data)
