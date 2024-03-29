from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("SR-BR", "Brokopondo"),
    Subdivision("SR-CM", "Commewijne"),
    Subdivision("SR-CR", "Coronie"),
    Subdivision("SR-MA", "Marowijne"),
    Subdivision("SR-NI", "Nickerie"),
    Subdivision("SR-PM", "Paramaribo"),
    Subdivision("SR-PR", "Para"),
    Subdivision("SR-SA", "Saramacca"),
    Subdivision("SR-SI", "Sipaliwini"),
    Subdivision("SR-WA", "Wanica"),
]
