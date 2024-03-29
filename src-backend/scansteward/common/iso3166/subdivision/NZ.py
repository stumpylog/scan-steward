from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("NZ-AUK", "Auckland"),
    Subdivision("NZ-BOP", "Bay of Plenty"),
    Subdivision("NZ-CAN", "Canterbury"),
    Subdivision("NZ-CIT", "Chatham Islands Territory"),
    Subdivision("NZ-GIS", "Gisborne"),
    Subdivision("NZ-HKB", "Hawke's Bay"),
    Subdivision("NZ-MBH", "Marlborough"),
    Subdivision("NZ-MWT", "Manawatū-Whanganui"),
    Subdivision("NZ-NSN", "Nelson"),
    Subdivision("NZ-NTL", "Northland"),
    Subdivision("NZ-OTA", "Otago"),
    Subdivision("NZ-STL", "Southland"),
    Subdivision("NZ-TAS", "Tasman"),
    Subdivision("NZ-TKI", "Taranaki"),
    Subdivision("NZ-WGN", "Greater Wellington"),
    Subdivision("NZ-WKO", "Waikato"),
    Subdivision("NZ-WTC", "West Coast"),
]
