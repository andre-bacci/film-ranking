from rest_framework import status


class ExternalServiceError(Exception):
    def __init__(self, service_name, status_code, message, *args):
        self.service_name = service_name
        self.status_code = status_code
        self.response_msg = message
        super().__init__(message, *args)


class ExternalServiceDataContractError(ExternalServiceError):
    def __init__(
        self, service_name, message, *args, status_code=status.HTTP_502_BAD_GATEWAY
    ):
        super().__init__(service_name, status_code, message, *args)


class ExternalServiceConnectionError(ExternalServiceError):
    def __init__(
        self, service_name, message, *args, status_code=status.HTTP_502_BAD_GATEWAY
    ):
        super().__init__(service_name, status_code, message, *args)
