from django.db import transaction
from rest_framework import filters, mixins, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from external_services.exceptions import ExternalServiceError

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
    def retrieve(self, request, film_id, format=None):
        try:
            film = self.film_service.get_film(film_id=film_id)
        except ExternalServiceError as e:
            return Response(
                data=e.response_msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        serializer = FilmSerializer(film)
        return Response(serializer.data)

    @transaction.atomic
    def search(self, request, format=None):
        query = request.query_params.get("search")
        page = int(request.query_params.get("page")) or 1
        length = int(request.query_params.get("length")) or 5
        try:
            films = self.film_service.search_films(
                query=query, page=page, length=length
            )
        except ExternalServiceError as e:
            return Response(
                data=e.response_msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        serializer = FilmSerializer(films, many=True)
        return Response(serializer.data)
