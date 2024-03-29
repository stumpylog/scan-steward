from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("CM-AD", "Adamaoua"),
    Subdivision("CM-CE", "Centre"),
    Subdivision("CM-EN", "Far North"),
    Subdivision("CM-ES", "East"),
    Subdivision("CM-LT", "Littoral"),
    Subdivision("CM-NO", "North"),
    Subdivision("CM-NW", "North-West"),
    Subdivision("CM-OU", "West"),
    Subdivision("CM-SU", "South"),
    Subdivision("CM-SW", "South-West"),
]
