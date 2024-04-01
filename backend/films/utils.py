from django.core.exceptions import ObjectDoesNotExist

from .models import Film
from .services import FilmService


def safely_get_film_by_id(film_id):
    try:
        film = Film.objects.get(tmdb_id=film_id)
        return film
    except ObjectDoesNotExist:
        film_service = FilmService()
        film = film_service.get_film(film_id)
        return film
