from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("CR-A", "Alajuela"),
    Subdivision("CR-C", "Cartago"),
    Subdivision("CR-G", "Guanacaste"),
    Subdivision("CR-H", "Heredia"),
    Subdivision("CR-L", "Limón"),
    Subdivision("CR-P", "Puntarenas"),
    Subdivision("CR-SJ", "San José"),
]
