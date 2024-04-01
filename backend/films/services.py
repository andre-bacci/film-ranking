from django.core.exceptions import ObjectDoesNotExist

from external_services.tmdb.converter import TMDBConverter
from external_services.tmdb.service import TMDBService

from .models import Credit, CreditRoleOptions, Film, Person


class BaseTMDBService:
    def __init__(self):
        self.tmdb_service = TMDBService()
        self.tmdb_converter = TMDBConverter()


class PersonService(BaseTMDBService):
    def create_person(self, info):
        imdb_id = info.get("imdb_id")
        if not imdb_id:
            info = self.tmdb_service.get_person_details(info.get("id"))
        person_data = self.tmdb_converter.convert_person_info_to_person_data(info)
        return Person.objects.create(**person_data)

    def get_or_create_person(self, info) -> Person:
        try:
            person = Person.objects.get(tmdb_id=info.get("id"))
        except ObjectDoesNotExist:
            person = self.create_person(info)
        if not person:
            return None
        return person


class CreditService(BaseTMDBService):
    def __init__(self):
        self.person_service = PersonService()
        super().__init__()

    def create_individual_credit(self, person, film_id, role):
        if not (person and film_id and role):
            return
        Credit.objects.get_or_create(person=person, film_id=film_id, role=role)

    def create_film_cast_credits(self, cast: dict, film_id: str):
        top_billed_cast_length = min(len(cast), 10)
        for cast_member_index in range(top_billed_cast_length):
            cast_member_info = cast[cast_member_index]
            person = self.person_service.get_or_create_person(cast_member_info)
            self.create_individual_credit(
                film_id=film_id, person=person, role=CreditRoleOptions.ACTOR
            )

    def create_film_crew_credits(self, crew: dict, film_id: str):
        for crew_member_info in crew:
            job = crew_member_info.get("job")
            role = self.tmdb_converter.convert_crew_job_to_credit_role(job)
            if not role:
                continue
            person = self.person_service.get_or_create_person(crew_member_info)
            self.create_individual_credit(film_id=film_id, person=person, role=role)

    def create_film_credits(self, film_id, credits):
        cast = credits.get("cast")
        self.create_film_cast_credits(cast, film_id=film_id)
        crew = credits.get("crew")
        self.create_film_crew_credits(crew, film_id=film_id)


class FilmService(BaseTMDBService):
    def __init__(self):
        self.credit_service = CreditService()
        self.person_service = PersonService()
        super().__init__()

    def get_film_id_type(self, film_id) -> str:
        if "tt" in film_id:
            return "imdb_id"
        else:
            return "tmdb_id"

    def create_film(self, response) -> Film:
        film_id = response.get("id")
        film_data = self.tmdb_converter.convert_movie_info_to_film_data(response)
        film = Film.objects.create(**film_data)
        credits = response.get("credits")
        if credits:
            self.credit_service.create_film_credits(film_id=film_id, credits=credits)
        return film

    def get_film(self, film_id) -> Film:
        film_id_type = self.get_film_id_type(film_id)

        try:
            if film_id_type == "imdb_id":
                film = Film.objects.get(imdb_id=film_id)
            elif film_id_type == "tmdb_id":
                film = Film.objects.get(tmdb_id=film_id)
            else:
                raise Exception("Invalid film id")
        except ObjectDoesNotExist:
            tmdb_film_response = self.tmdb_service.get_film_details(
                film_id=film_id, append_to_response="credits"
            )
            film = self.create_film(response=tmdb_film_response)

        if not film.directed_by_queryset or not film.written_by_queryset:
            tmdb_credit_response = self.tmdb_service.get_film_credits(film_id=film_id)
            self.credit_service.create_film_credits(
                film_id=film_id, credits=tmdb_credit_response
            )

        return film
