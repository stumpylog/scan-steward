from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("GL-AV", "Avannaata Kommunia"),
    Subdivision("GL-KU", "Kommune Kujalleq"),
    Subdivision("GL-QE", "Qeqqata Kommunia"),
    Subdivision("GL-QT", "Kommune Qeqertalik"),
    Subdivision("GL-SM", "Kommuneqarfik Sermersooq"),
]
