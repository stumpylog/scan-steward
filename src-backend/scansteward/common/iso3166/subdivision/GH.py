from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("GH-AA", "Greater Accra"),
    Subdivision("GH-AF", "Ahafo"),
    Subdivision("GH-AH", "Ashanti"),
    Subdivision("GH-BE", "Bono East"),
    Subdivision("GH-BO", "Bono"),
    Subdivision("GH-CP", "Central"),
    Subdivision("GH-EP", "Eastern"),
    Subdivision("GH-NE", "North East"),
    Subdivision("GH-NP", "Northern"),
    Subdivision("GH-OT", "Oti"),
    Subdivision("GH-SV", "Savannah"),
    Subdivision("GH-TV", "Volta"),
    Subdivision("GH-UE", "Upper East"),
    Subdivision("GH-UW", "Upper West"),
    Subdivision("GH-WN", "Western North"),
    Subdivision("GH-WP", "Western"),
]
