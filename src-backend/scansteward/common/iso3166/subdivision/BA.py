from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("BA-BIH", "Federacija Bosne i Hercegovine"),
    Subdivision("BA-BRC", "Brčko distrikt"),
    Subdivision("BA-SRP", "Republika Srpska"),
]
