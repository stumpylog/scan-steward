from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("SL-E", "Eastern"),
    Subdivision("SL-N", "Northern"),
    Subdivision("SL-NW", "North Western"),
    Subdivision("SL-S", "Southern"),
    Subdivision("SL-W", "Western Area (Freetown)"),
]
