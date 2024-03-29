from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("ZM-01", "Western"),
    Subdivision("ZM-02", "Central"),
    Subdivision("ZM-03", "Eastern"),
    Subdivision("ZM-04", "Luapula"),
    Subdivision("ZM-05", "Northern"),
    Subdivision("ZM-06", "North-Western"),
    Subdivision("ZM-07", "Southern"),
    Subdivision("ZM-08", "Copperbelt"),
    Subdivision("ZM-09", "Lusaka"),
    Subdivision("ZM-10", "Muchinga"),
]
