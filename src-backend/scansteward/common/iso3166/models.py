from collections.abc import Generator
from dataclasses import dataclass
from dataclasses import field
from functools import cached_property


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
        init=False,
        default_factory=dict,
        repr=False,
    )
    subdivisions_loaded: bool = field(init=False, default=False, repr=False)

    def contains_subdivision(self, subdivision_code: str) -> bool:
        self._check_and_load()
        return subdivision_code in self.actual_subdivisions

    def _check_and_load(self):
        if not self.subdivisions_loaded:
            from scansteward.common.iso3166.subdivision import (  # noqa: I001
                get_subdivisions_by_country_code,
            )

            for sub in get_subdivisions_by_country_code(self.alpha2):
                self.actual_subdivisions[sub.code] = sub

    @property
    def subdivisions(self) -> Generator[Subdivision, None, None]:
        self._check_and_load()
        for sub in self.actual_subdivisions:
            yield self.actual_subdivisions[sub]

    def get_subdivision(self, subdivision_code: str) -> Subdivision | None:
        self._check_and_load()
        return self.actual_subdivisions.get(subdivision_code)

    def get_subdivision_name(self, subdivision_code: str) -> str | None:
        self._check_and_load()
        subdivision = self.get_subdivision(subdivision_code)
        if subdivision:
            return subdivision.name
        return None
