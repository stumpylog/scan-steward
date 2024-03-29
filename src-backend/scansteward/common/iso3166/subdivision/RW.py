from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("RW-01", "City of Kigali"),
    Subdivision("RW-02", "Eastern"),
    Subdivision("RW-03", "Northern"),
    Subdivision("RW-04", "Western"),
    Subdivision("RW-05", "Southern"),
]
