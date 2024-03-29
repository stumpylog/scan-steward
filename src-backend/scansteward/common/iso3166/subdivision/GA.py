from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("GA-1", "Estuaire"),
    Subdivision("GA-2", "Haut-Ogooué"),
    Subdivision("GA-3", "Moyen-Ogooué"),
    Subdivision("GA-4", "Ngounié"),
    Subdivision("GA-5", "Nyanga"),
    Subdivision("GA-6", "Ogooué-Ivindo"),
    Subdivision("GA-7", "Ogooué-Lolo"),
    Subdivision("GA-8", "Ogooué-Maritime"),
    Subdivision("GA-9", "Woleu-Ntem"),
]
