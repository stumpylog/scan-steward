from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("BO-B", "El Beni"),
    Subdivision("BO-C", "Cochabamba"),
    Subdivision("BO-H", "Chuquisaca"),
    Subdivision("BO-L", "La Paz"),
    Subdivision("BO-N", "Pando"),
    Subdivision("BO-O", "Oruro"),
    Subdivision("BO-P", "Potosí"),
    Subdivision("BO-S", "Santa Cruz"),
    Subdivision("BO-T", "Tarija"),
]
