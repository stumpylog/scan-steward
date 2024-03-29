from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("BZ-BZ", "Belize"),
    Subdivision("BZ-CY", "Cayo"),
    Subdivision("BZ-CZL", "Corozal"),
    Subdivision("BZ-OW", "Orange Walk"),
    Subdivision("BZ-SC", "Stann Creek"),
    Subdivision("BZ-TOL", "Toledo"),
]
