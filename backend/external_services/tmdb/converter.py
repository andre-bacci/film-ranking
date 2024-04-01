from films.models import CreditRoleOptions


class TMDBConverter:
    crew_job_to_credit_role_map = {
        "Director": CreditRoleOptions.DIRECTOR,
        "Screenplay": CreditRoleOptions.WRITER,
        "Writer": CreditRoleOptions.WRITER,
    }

    def convert_movie_info_to_film_data(self, movie_info):
        film_data = {
            "imdb_id": movie_info.get("imdb_id"),
            "tmdb_id": movie_info.get("id"),
            "title": movie_info.get("title"),
            "original_title": movie_info.get("original_title"),
            "release_date": movie_info.get("release_date"),
            "runtime": movie_info.get("runtime"),
            "synopsis": movie_info.get("overview"),
            "credits": movie_info.get("credits"),
        }
        return film_data

    def convert_person_info_to_person_data(self, person_info):
        person_data = {
            "imdb_id": person_info.get("imdb_id"),
            "tmdb_id": person_info.get("id"),
            "name": person_info.get("name"),
            "bio": person_info.get("biography"),
            "date_of_birth": person_info.get("birthday"),
            "date_of_death": person_info.get("deathday"),
        }
        return person_data

    def convert_crew_job_to_credit_role(self, job):
        if job not in self.crew_job_to_credit_role_map:
            return None
        return self.crew_job_to_credit_role_map[job]
