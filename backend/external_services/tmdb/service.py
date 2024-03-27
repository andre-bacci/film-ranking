import logging

from django.conf import settings

from ..common import BaseService

logger = logging.getLogger(__name__)


class TMDBService(BaseService):
    def __init__(self, *args, **kwargs):
        self.base_url = "https://api.themoviedb.org/3"
        self.film_details_url = f"{self.base_url}/movie/{{film_id}}"
        self.film_credits_url = f"{self.base_url}/movie/{{film_id}}/credits"
        self.person_details_url = f"{self.base_url}/person/{{person_id}}"
        super().__init__(*args, **kwargs)

    def get_auth_header(self):
        return {"Authorization": f"Bearer {settings.TMDB_API_TOKEN}"}

    def get_timeout(self):
        return settings.TMDB_REQUEST_TIMEOUT

    def get_film_details(self, film_id, append_to_response: str = None):
        url = self.film_details_url.format(film_id=film_id)
        params = {}
        if append_to_response:
            params["append_to_response"] = append_to_response
        return self._request_get(
            url,
            headers=self.get_auth_header(),
            timeout=self.get_timeout(),
            params=params,
        )

    def get_film_credits(self, film_id, append_to_response: str = None):
        url = self.film_credits_url.format(film_id=film_id)
        params = {}
        if append_to_response:
            params["append_to_response"] = append_to_response
        return self._request_get(
            url,
            headers=self.get_auth_header(),
            timeout=self.get_timeout(),
            params=params,
        )

    def get_person_details(self, person_id, append_to_response: str = None):
        url = self.person_details_url.format(person_id=person_id)
        params = {}
        if append_to_response:
            params["append_to_response"] = append_to_response
        return self._request_get(
            url,
            headers=self.get_auth_header(),
            timeout=self.get_timeout(),
            params=params,
        )
