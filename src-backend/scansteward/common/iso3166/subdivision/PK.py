from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("PK-BA", "Balochistan"),
    Subdivision("PK-GB", "Gilgit-Baltistan"),
    Subdivision("PK-IS", "Islamabad"),
    Subdivision("PK-JK", "Azad Jammu and Kashmir"),
    Subdivision("PK-KP", "Khyber Pakhtunkhwa"),
    Subdivision("PK-PB", "Punjab"),
    Subdivision("PK-SD", "Sindh"),
]
