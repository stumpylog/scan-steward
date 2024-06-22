from typing import Protocol

from django.http import HttpResponse


class PersonGeneratorProtocol(Protocol):
    def __call__(self, *, with_description: bool = False) -> int:  # type: ignore[return]
        pass


class LocationGeneratorProtocol(Protocol):
    def __call__(
        self,
        country: str,
        subdivision: str | None = None,
        city: str | None = None,
        location: str | None = None,
    ) -> int:  # type: ignore[return]
        pass


class AlbumApiGeneratorProtocol(Protocol):
    def __call__(self, name: str | None = None, description: str | None = None) -> HttpResponse:  # type: ignore[return]
        pass
