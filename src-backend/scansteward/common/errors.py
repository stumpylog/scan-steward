from http import HTTPStatus

from ninja.errors import HttpError


class Http400Error(HttpError):
    """
    An error with BAD_REQUEST status code and the provided message.
    """

    def __init__(self, message: str) -> None:
        super().__init__(HTTPStatus.BAD_REQUEST, message)
