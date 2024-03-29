from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("SK-BC", "Banskobystrický kraj"),
    Subdivision("SK-BL", "Bratislavský kraj"),
    Subdivision("SK-KI", "Košický kraj"),
    Subdivision("SK-NI", "Nitriansky kraj"),
    Subdivision("SK-PV", "Prešovský kraj"),
    Subdivision("SK-TA", "Trnavský kraj"),
    Subdivision("SK-TC", "Trenčiansky kraj"),
    Subdivision("SK-ZI", "Žilinský kraj"),
]
