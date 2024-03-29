from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("SG-01", "Central Singapore"),
    Subdivision("SG-02", "North East"),
    Subdivision("SG-03", "North West"),
    Subdivision("SG-04", "South East"),
    Subdivision("SG-05", "South West"),
]
