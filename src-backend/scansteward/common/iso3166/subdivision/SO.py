from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("SO-AW", "Awdal"),
    Subdivision("SO-BK", "Bakool"),
    Subdivision("SO-BN", "Banaadir"),
    Subdivision("SO-BR", "Bari"),
    Subdivision("SO-BY", "Bay"),
    Subdivision("SO-GA", "Galguduud"),
    Subdivision("SO-GE", "Gedo"),
    Subdivision("SO-HI", "Hiiraan"),
    Subdivision("SO-JD", "Jubbada Dhexe"),
    Subdivision("SO-JH", "Jubbada Hoose"),
    Subdivision("SO-MU", "Mudug"),
    Subdivision("SO-NU", "Nugaal"),
    Subdivision("SO-SA", "Sanaag"),
    Subdivision("SO-SD", "Shabeellaha Dhexe"),
    Subdivision("SO-SH", "Shabeellaha Hoose"),
    Subdivision("SO-SO", "Sool"),
    Subdivision("SO-TO", "Togdheer"),
    Subdivision("SO-WO", "Woqooyi Galbeed"),
]
