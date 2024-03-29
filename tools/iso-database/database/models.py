from dataclasses import dataclass, field
from functools import cached_property, lru_cache

from typing import Generator


@dataclass(slots=True, frozen=True)
class Subdivision:

    code: str
    name: str

    @cached_property
    def country_alpha_2(self):
        return self.code.split("-")[0]


@dataclass(slots=True)
class Country:

    alpha2: str
    name: str
    actual_subdivisions: dict[str, Subdivision] = field(
        init=False, default_factory=dict, repr=False
    )
    subdivisions_loaded: bool = field(init=False, default=False, repr=False)

    @lru_cache
    def __contains__(self, subdivision_code: str) -> bool:
        self._check_and_load()
        return subdivision_code in self.actual_subdivisions

    def _check_and_load(self):
        if not self.subdivisions_loaded:
            from .subdivision import get_subdivisions_by_country_code

            for sub in get_subdivisions_by_country_code(self.alpha2):
                self.actual_subdivisions[sub.code] = sub

    @property
    def subdivisions(self) -> Generator[Subdivision, None, None]:
        self._check_and_load()
        for sub in self.actual_subdivisions:
            yield self.actual_subdivisions[sub]

    @lru_cache
    def get_subdivision(self, subdivision_code: str) -> Subdivision | None:
        self._check_and_load()
        return self.actual_subdivisions.get(subdivision_code)

    @lru_cache
    def get_subdivision_name(self, subdivision_code: str) -> str | None:
        self._check_and_load()
        subdivision = self.get_subdivision(subdivision_code)
        if subdivision:
            return subdivision.name
        return None
