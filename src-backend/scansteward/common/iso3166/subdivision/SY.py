from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("SY-DI", "Dimashq"),
    Subdivision("SY-DR", "Dar'ā"),
    Subdivision("SY-DY", "Dayr az Zawr"),
    Subdivision("SY-HA", "Al Ḩasakah"),
    Subdivision("SY-HI", "Ḩimş"),
    Subdivision("SY-HL", "Ḩalab"),
    Subdivision("SY-HM", "Ḩamāh"),
    Subdivision("SY-ID", "Idlib"),
    Subdivision("SY-LA", "Al Lādhiqīyah"),
    Subdivision("SY-QU", "Al Qunayţirah"),
    Subdivision("SY-RA", "Ar Raqqah"),
    Subdivision("SY-RD", "Rīf Dimashq"),
    Subdivision("SY-SU", "As Suwaydā'"),
    Subdivision("SY-TA", "Ţarţūs"),
]
