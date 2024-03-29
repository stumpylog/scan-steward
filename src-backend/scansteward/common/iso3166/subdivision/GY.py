from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("GY-BA", "Barima-Waini"),
    Subdivision("GY-CU", "Cuyuni-Mazaruni"),
    Subdivision("GY-DE", "Demerara-Mahaica"),
    Subdivision("GY-EB", "East Berbice-Corentyne"),
    Subdivision("GY-ES", "Essequibo Islands-West Demerara"),
    Subdivision("GY-MA", "Mahaica-Berbice"),
    Subdivision("GY-PM", "Pomeroon-Supenaam"),
    Subdivision("GY-PT", "Potaro-Siparuni"),
    Subdivision("GY-UD", "Upper Demerara-Berbice"),
    Subdivision("GY-UT", "Upper Takutu-Upper Essequibo"),
]
