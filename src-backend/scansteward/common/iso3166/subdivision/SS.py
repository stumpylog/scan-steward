from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("SS-BN", "Northern Bahr el Ghazal"),
    Subdivision("SS-BW", "Western Bahr el Ghazal"),
    Subdivision("SS-EC", "Central Equatoria"),
    Subdivision("SS-EE", "Eastern Equatoria"),
    Subdivision("SS-EW", "Western Equatoria"),
    Subdivision("SS-JG", "Jonglei"),
    Subdivision("SS-LK", "Lakes"),
    Subdivision("SS-NU", "Upper Nile"),
    Subdivision("SS-UY", "Unity"),
    Subdivision("SS-WR", "Warrap"),
]
