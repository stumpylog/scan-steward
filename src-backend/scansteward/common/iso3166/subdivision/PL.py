from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("PL-02", "Dolnośląskie"),
    Subdivision("PL-04", "Kujawsko-Pomorskie"),
    Subdivision("PL-06", "Lubelskie"),
    Subdivision("PL-08", "Lubuskie"),
    Subdivision("PL-10", "Łódzkie"),
    Subdivision("PL-12", "Małopolskie"),
    Subdivision("PL-14", "Mazowieckie"),
    Subdivision("PL-16", "Opolskie"),
    Subdivision("PL-18", "Podkarpackie"),
    Subdivision("PL-20", "Podlaskie"),
    Subdivision("PL-22", "Pomorskie"),
    Subdivision("PL-24", "Śląskie"),
    Subdivision("PL-26", "Świętokrzyskie"),
    Subdivision("PL-28", "Warmińsko-Mazurskie"),
    Subdivision("PL-30", "Wielkopolskie"),
    Subdivision("PL-32", "Zachodniopomorskie"),
]
