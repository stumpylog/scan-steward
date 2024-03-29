from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("GM-B", "Banjul"),
    Subdivision("GM-L", "Lower River"),
    Subdivision("GM-M", "Central River"),
    Subdivision("GM-N", "North Bank"),
    Subdivision("GM-U", "Upper River"),
    Subdivision("GM-W", "Western"),
]
