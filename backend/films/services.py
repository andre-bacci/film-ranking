from django.core.exceptions import ObjectDoesNotExist

from external_services.tmdb import TMDBService

from .models import Film


class FilmService:
    def __init__(self):
        self.tmdb_service = TMDBService()

    def _create_film_from_response(self, response):
        film = Film.objects.create(
            imdb_id=response.get("imdb_id"),
            tmdb_id=response.get("id"),
            title=response.get("title"),
            original_title=response.get("original_title"),
            release_date=response.get("release_date"),
            runtime=response.get("runtime"),
            synopsis=response.get("overview"),
        )
        return film

    def get_film(self, imdb_id):
        try:
            film = Film.objects.get(imdb_id=imdb_id)
        except ObjectDoesNotExist:
            tmdb_film_response = self.tmdb_service.get_film_details(film_id=imdb_id)
            film = self._create_film_from_response(tmdb_film_response)

        return film
