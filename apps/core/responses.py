from collections import OrderedDict

from rest_framework import status
from rest_framework.response import Response


class CustomResponse(Response):
    def __init__(self, message=None, data=None, status=200, *args, **kwargs):

        # Filtering kwargs
        drf_response_kwargs = (
            "data",
            "status",
            "template_name",
            "headers",
            "exception",
            "content_type",
        )
        drf_response_kwargs = {
            key: value for key, value in kwargs.items() if key in drf_response_kwargs
        }
        super().__init__(status=status, data=data, **drf_response_kwargs)
        self.message = message
        self.status = status

        # JSON OUTPUT
        self.data = OrderedDict()
        self.data.update(
            {
                "status": self.status,
                "message": message,
                "result": data,
            }
        )

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.data


class CreateResponse(CustomResponse):
    ...


class ListResponse(CustomResponse):
    ...


class RetrieveResponse(CustomResponse):
    ...


class UpdateResponse(CustomResponse):
    ...


class DeleteResponse(CustomResponse):
    ...


class SuccessResponse(CustomResponse):
    def __init__(
        self, message=None, data=None, status=status.HTTP_200_OK, *args, **kwargs
    ):
        super().__init__(message, data, status, *args, **kwargs)


class ErrorResponse(CustomResponse):
    def __init__(
        self,
        message=None,
        data=None,
        status=status.HTTP_400_BAD_REQUEST,
        *args,
        **kwargs
    ):
        super().__init__(message, data, status, *args, **kwargs)
