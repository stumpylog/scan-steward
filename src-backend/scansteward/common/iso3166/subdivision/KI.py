from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("KI-G", "Gilbert Islands"),
    Subdivision("KI-L", "Line Islands"),
    Subdivision("KI-P", "Phoenix Islands"),
]
