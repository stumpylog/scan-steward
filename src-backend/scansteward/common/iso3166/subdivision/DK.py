from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("DK-81", "Nordjylland"),
    Subdivision("DK-82", "Midtjylland"),
    Subdivision("DK-83", "Syddanmark"),
    Subdivision("DK-84", "Hovedstaden"),
    Subdivision("DK-85", "Sjælland"),
]
