from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("SB-CE", "Central"),
    Subdivision("SB-CH", "Choiseul"),
    Subdivision("SB-CT", "Capital Territory (Honiara)"),
    Subdivision("SB-GU", "Guadalcanal"),
    Subdivision("SB-IS", "Isabel"),
    Subdivision("SB-MK", "Makira-Ulawa"),
    Subdivision("SB-ML", "Malaita"),
    Subdivision("SB-RB", "Rennell and Bellona"),
    Subdivision("SB-TE", "Temotu"),
    Subdivision("SB-WE", "Western"),
]
