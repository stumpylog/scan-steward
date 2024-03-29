from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("MG-A", "Toamasina"),
    Subdivision("MG-D", "Antsiranana"),
    Subdivision("MG-F", "Fianarantsoa"),
    Subdivision("MG-M", "Mahajanga"),
    Subdivision("MG-T", "Antananarivo"),
    Subdivision("MG-U", "Toliara"),
]
