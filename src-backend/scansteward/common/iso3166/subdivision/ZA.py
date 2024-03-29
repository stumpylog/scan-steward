from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("ZA-EC", "Eastern Cape"),
    Subdivision("ZA-FS", "Free State"),
    Subdivision("ZA-GP", "Gauteng"),
    Subdivision("ZA-KZN", "Kwazulu-Natal"),
    Subdivision("ZA-LP", "Limpopo"),
    Subdivision("ZA-MP", "Mpumalanga"),
    Subdivision("ZA-NC", "Northern Cape"),
    Subdivision("ZA-NW", "North-West"),
    Subdivision("ZA-WC", "Western Cape"),
]
