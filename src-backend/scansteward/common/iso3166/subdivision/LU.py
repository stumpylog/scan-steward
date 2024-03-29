from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("LU-CA", "Capellen"),
    Subdivision("LU-CL", "Clervaux"),
    Subdivision("LU-DI", "Diekirch"),
    Subdivision("LU-EC", "Echternach"),
    Subdivision("LU-ES", "Esch-sur-Alzette"),
    Subdivision("LU-GR", "Grevenmacher"),
    Subdivision("LU-LU", "Luxembourg"),
    Subdivision("LU-ME", "Mersch"),
    Subdivision("LU-RD", "Redange"),
    Subdivision("LU-RM", "Remich"),
    Subdivision("LU-VD", "Vianden"),
    Subdivision("LU-WI", "Wiltz"),
]
