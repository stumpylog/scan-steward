from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("AO-BGO", "Bengo"),
    Subdivision("AO-BGU", "Benguela"),
    Subdivision("AO-BIE", "Bié"),
    Subdivision("AO-CAB", "Cabinda"),
    Subdivision("AO-CCU", "Cuando Cubango"),
    Subdivision("AO-CNN", "Cunene"),
    Subdivision("AO-CNO", "Cuanza-Norte"),
    Subdivision("AO-CUS", "Cuanza-Sul"),
    Subdivision("AO-HUA", "Huambo"),
    Subdivision("AO-HUI", "Huíla"),
    Subdivision("AO-LNO", "Lunda-Norte"),
    Subdivision("AO-LSU", "Lunda-Sul"),
    Subdivision("AO-LUA", "Luanda"),
    Subdivision("AO-MAL", "Malange"),
    Subdivision("AO-MOX", "Moxico"),
    Subdivision("AO-NAM", "Namibe"),
    Subdivision("AO-UIG", "Uíge"),
    Subdivision("AO-ZAI", "Zaire"),
]
