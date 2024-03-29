from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("VU-MAP", "Malampa"),
    Subdivision("VU-PAM", "Pénama"),
    Subdivision("VU-SAM", "Sanma"),
    Subdivision("VU-SEE", "Shéfa"),
    Subdivision("VU-TAE", "Taféa"),
    Subdivision("VU-TOB", "Torba"),
]
