from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("SV-AH", "Ahuachapán"),
    Subdivision("SV-CA", "Cabañas"),
    Subdivision("SV-CH", "Chalatenango"),
    Subdivision("SV-CU", "Cuscatlán"),
    Subdivision("SV-LI", "La Libertad"),
    Subdivision("SV-MO", "Morazán"),
    Subdivision("SV-PA", "La Paz"),
    Subdivision("SV-SA", "Santa Ana"),
    Subdivision("SV-SM", "San Miguel"),
    Subdivision("SV-SO", "Sonsonate"),
    Subdivision("SV-SS", "San Salvador"),
    Subdivision("SV-SV", "San Vicente"),
    Subdivision("SV-UN", "La Unión"),
    Subdivision("SV-US", "Usulután"),
]
