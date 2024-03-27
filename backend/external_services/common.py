import logging

import requests

from .exceptions import ExternalServiceConnectionError, ExternalServiceError

logger = logging.getLogger(__name__)


def handle_connection_errors(func):
    def handle_it(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            service_name = self.__class__.__name__
            message = str(e) or "Service unavailable"
            raise ExternalServiceConnectionError(service_name, message) from None

    return handle_it


class BaseService:
    @handle_connection_errors
    def _request_get(self, url, headers=None, timeout=10, params=None, **kwargs):
        response = requests.get(
            url, params=params, headers=headers, timeout=timeout, **kwargs
        )
        logger.info(
            "[%s] Called %s",
            self.__class__.__name__,
            url,
        )

        return self._get_valid_json_response(response)

    def _get_valid_json_response(self, response):
        try:
            response_msg = response.json()
        except ValueError:
            response_msg = response.reason

        if response.ok:
            return response_msg
        service_name = self.__class__.__name__
        raise ExternalServiceError(service_name, response.status_code, response_msg)
