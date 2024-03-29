from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("SH-AC", "Ascension"),
    Subdivision("SH-HL", "Saint Helena"),
    Subdivision("SH-TA", "Tristan da Cunha"),
]
