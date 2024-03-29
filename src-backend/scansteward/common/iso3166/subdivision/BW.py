from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("BW-CE", "Central"),
    Subdivision("BW-CH", "Chobe"),
    Subdivision("BW-FR", "Francistown"),
    Subdivision("BW-GA", "Gaborone"),
    Subdivision("BW-GH", "Ghanzi"),
    Subdivision("BW-JW", "Jwaneng"),
    Subdivision("BW-KG", "Kgalagadi"),
    Subdivision("BW-KL", "Kgatleng"),
    Subdivision("BW-KW", "Kweneng"),
    Subdivision("BW-LO", "Lobatse"),
    Subdivision("BW-NE", "North East"),
    Subdivision("BW-NW", "North West"),
    Subdivision("BW-SE", "South East"),
    Subdivision("BW-SO", "Southern"),
    Subdivision("BW-SP", "Selibe Phikwe"),
    Subdivision("BW-ST", "Sowa Town"),
]
