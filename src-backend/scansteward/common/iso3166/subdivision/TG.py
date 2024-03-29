from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("TG-C", "Centrale"),
    Subdivision("TG-K", "Kara"),
    Subdivision("TG-M", "Maritime (Région)"),
    Subdivision("TG-P", "Plateaux"),
    Subdivision("TG-S", "Savanes"),
]
