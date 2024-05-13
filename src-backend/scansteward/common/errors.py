from http import HTTPStatus

from ninja.errors import HttpError


class HttpBadRequestError(HttpError):
    """
    An error with BAD_REQUEST status code and the provided message.
    """

    def __init__(self, message: str) -> None:
        super().__init__(HTTPStatus.BAD_REQUEST, message)


class HttpConflictError(HttpError):
    """
    An error with CONFLICT status code and the provided message.
    """

    def __init__(self, message: str) -> None:
        super().__init__(HTTPStatus.CONFLICT, message)


class HttpUnprocessableEntityError(HttpError):
    """
    An error with UNPROCESSABLE status code and the provided message.
    """

    def __init__(self, message: str) -> None:
        super().__init__(HTTPStatus.UNPROCESSABLE_ENTITY, message)
