import traceback

from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

from apps.core.responses import ErrorResponse


def custom_exception_handler(exc: Exception, context: dict):
    """Custom API exception handler"""

    if isinstance(exc, CustomAPIException):
        return ErrorResponse(
            message=exc.error_message, data=exc.error_data, status=exc.status_code
        )

    response = exception_handler(exc, context)
    if settings.DEBUG:
        if isinstance(response.data, list):
            response.data.append({"exception_detail": traceback.format_exc()})
        elif isinstance(response.data, dict):
            response.data.update({"exception_detail": traceback.format_exc()})
        else:
            response.data = {"exception_detail": traceback.format_exc()}

    return ErrorResponse(
        message="Unexpected Error", status=response.status_code, data=response.data
    )


class CustomAPIException(APIException):
    def __init__(
        self,
        error_message="Error",
        error_data=None,
        status_code=status.HTTP_400_BAD_REQUEST,
        **kwargs
    ):
        self.error_message = error_message
        self.error_data = error_data
        self.status_code = status_code
        super().__init__(**kwargs)


class DataInvalidException(CustomAPIException):
    ...


class MaximumLimitException(CustomAPIException):
    ...


class ErrorException(CustomAPIException):
    ...
