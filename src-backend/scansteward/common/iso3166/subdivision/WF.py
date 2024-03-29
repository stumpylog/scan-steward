from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("WF-AL", "Alo"),
    Subdivision("WF-SG", "Sigave"),
    Subdivision("WF-UV", "Uvea"),
]
