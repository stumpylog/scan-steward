from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("MM-01", "Sagaing"),
    Subdivision("MM-02", "Bago"),
    Subdivision("MM-03", "Magway"),
    Subdivision("MM-04", "Mandalay"),
    Subdivision("MM-05", "Tanintharyi"),
    Subdivision("MM-06", "Yangon"),
    Subdivision("MM-07", "Ayeyarwady"),
    Subdivision("MM-11", "Kachin"),
    Subdivision("MM-12", "Kayah"),
    Subdivision("MM-13", "Kayin"),
    Subdivision("MM-14", "Chin"),
    Subdivision("MM-15", "Mon"),
    Subdivision("MM-16", "Rakhine"),
    Subdivision("MM-17", "Shan"),
    Subdivision("MM-18", "Nay Pyi Taw"),
]
