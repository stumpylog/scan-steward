from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("FM-KSA", "Kosrae"),
    Subdivision("FM-PNI", "Pohnpei"),
    Subdivision("FM-TRK", "Chuuk"),
    Subdivision("FM-YAP", "Yap"),
]
