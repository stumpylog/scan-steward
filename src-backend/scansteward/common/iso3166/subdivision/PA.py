from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("PA-1", "Bocas del Toro"),
    Subdivision("PA-10", "Panamá Oeste"),
    Subdivision("PA-2", "Coclé"),
    Subdivision("PA-3", "Colón"),
    Subdivision("PA-4", "Chiriquí"),
    Subdivision("PA-5", "Darién"),
    Subdivision("PA-6", "Herrera"),
    Subdivision("PA-7", "Los Santos"),
    Subdivision("PA-8", "Panamá"),
    Subdivision("PA-9", "Veraguas"),
    Subdivision("PA-EM", "Emberá"),
    Subdivision("PA-KY", "Guna Yala"),
    Subdivision("PA-NB", "Ngäbe-Buglé"),
    Subdivision("PA-NT", "Naso Tjër Di"),
]
