from django.core.exceptions import ObjectDoesNotExist

from external_services.tmdb import TMDBService

from .models import Credit, Film, Person


class FilmService:
    def __init__(self):
        self.tmdb_service = TMDBService()

    def _create_person(self, info):
        imdb_id = info.get("imdb_id")
        if not imdb_id:
            info = self.tmdb_service.get_person_details(info.get("id"))
        if not info.get("imdb_id"):
            return None
        return Person.objects.create(
            imdb_id=info.get("imdb_id"),
            tmdb_id=info.get("id"),
            name=info.get("name"),
            bio=info.get("biography"),
            date_of_birth=info.get("birthday"),
            date_of_death=info.get("deathday"),
        )

    def _get_or_create_credit(self, film_id: str, person: Person, role: str):
        Credit.objects.get_or_create(
            person_id=person.imdb_id, film_id=film_id, role=role
        )

    def _add_credit_to_person(self, person_info, film_id, role):
        try:
            person = Person.objects.get(tmdb_id=person_info.get("id"))
        except ObjectDoesNotExist:
            person = self._create_person(person_info)
        if not person:
            return
        self._get_or_create_credit(film_id=film_id, person=person, role=role)

    def _add_top_billed_cast_to_film(self, cast: dict, film_id: str):
        top_billed_cast_length = min(len(cast), 10)
        for cast_member_index in range(top_billed_cast_length):
            cast_member_info = cast[cast_member_index]
            self._add_credit_to_person(
                film_id=film_id, person_info=cast_member_info, role="actor"
            )

    def _add_crew_to_film(self, crew: dict, film_id: str):
        jobs_to_add = ["Screenplay", "Director"]
        for crew_member in crew:
            job = crew_member.get("job")
            if job not in jobs_to_add:
                continue
            if job == "Screenplay":
                self._add_credit_to_person(
                    film_id=film_id, person_info=crew_member, role="writer"
                )
            if job == "Director":
                self._add_credit_to_person(
                    film_id=film_id, person_info=crew_member, role="director"
                )

    def _add_credits_to_film(self, film_id, credits):
        cast = credits.get("cast")
        self._add_top_billed_cast_to_film(cast, film_id=film_id)
        crew = credits.get("crew")
        self._add_crew_to_film(crew, film_id=film_id)

    def _create_film_from_response(self, response, has_credits: bool = False) -> Film:
        # TODO: Create converter
        film_id = response.get("imdb_id")
        film = Film.objects.create(
            imdb_id=response.get("imdb_id"),
            tmdb_id=response.get("id"),
            title=response.get("title"),
            original_title=response.get("original_title"),
            release_date=response.get("release_date"),
            runtime=response.get("runtime"),
            synopsis=response.get("overview"),
        )
        if has_credits:
            credits = response.get("credits", {})
            self._add_credits_to_film(film_id=film_id, credits=credits)
        return film

    def get_film(self, imdb_id) -> Film:
        try:
            film = Film.objects.get(imdb_id=imdb_id)
        except ObjectDoesNotExist:
            tmdb_film_response = self.tmdb_service.get_film_details(
                film_id=imdb_id, append_to_response="credits"
            )
            film = self._create_film_from_response(tmdb_film_response, has_credits=True)

        if not film.directed_by:
            tmdb_credit_response = self.tmdb_service.get_film_credits(film_id=imdb_id)
            self._add_credits_to_film(film_id=imdb_id, credits=tmdb_credit_response)

        return film
