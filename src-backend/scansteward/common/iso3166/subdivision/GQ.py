from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("GQ-AN", "Annobon"),
    Subdivision("GQ-BN", "Bioko Nord"),
    Subdivision("GQ-BS", "Bioko Sud"),
    Subdivision("GQ-C", "Région Continentale"),
    Subdivision("GQ-CS", "Centro Sud"),
    Subdivision("GQ-DJ", "Djibloho"),
    Subdivision("GQ-I", "Région Insulaire"),
    Subdivision("GQ-KN", "Kié-Ntem"),
    Subdivision("GQ-LI", "Littoral"),
    Subdivision("GQ-WN", "Wele-Nzas"),
]
