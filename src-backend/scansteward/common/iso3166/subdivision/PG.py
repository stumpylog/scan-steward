from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("PG-CPK", "Chimbu"),
    Subdivision("PG-CPM", "Central"),
    Subdivision("PG-EBR", "East New Britain"),
    Subdivision("PG-EHG", "Eastern Highlands"),
    Subdivision("PG-EPW", "Enga"),
    Subdivision("PG-ESW", "East Sepik"),
    Subdivision("PG-GPK", "Gulf"),
    Subdivision("PG-HLA", "Hela"),
    Subdivision("PG-JWK", "Jiwaka"),
    Subdivision("PG-MBA", "Milne Bay"),
    Subdivision("PG-MPL", "Morobe"),
    Subdivision("PG-MPM", "Madang"),
    Subdivision("PG-MRL", "Manus"),
    Subdivision("PG-NCD", "National Capital District (Port Moresby)"),
    Subdivision("PG-NIK", "New Ireland"),
    Subdivision("PG-NPP", "Northern"),
    Subdivision("PG-NSB", "Bougainville"),
    Subdivision("PG-SAN", "West Sepik"),
    Subdivision("PG-SHM", "Southern Highlands"),
    Subdivision("PG-WBK", "West New Britain"),
    Subdivision("PG-WHM", "Western Highlands"),
    Subdivision("PG-WPD", "Western"),
]
