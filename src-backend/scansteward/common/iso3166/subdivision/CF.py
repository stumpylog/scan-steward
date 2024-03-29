from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("CF-AC", "Ouham"),
    Subdivision("CF-BB", "Bamingui-Bangoran"),
    Subdivision("CF-BGF", "Bangui"),
    Subdivision("CF-BK", "Basse-Kotto"),
    Subdivision("CF-HK", "Haute-Kotto"),
    Subdivision("CF-HM", "Haut-Mbomou"),
    Subdivision("CF-HS", "Haute-Sangha / Mambéré-Kadéï"),
    Subdivision("CF-KB", "Gribingui"),
    Subdivision("CF-KG", "Kémo-Gribingui"),
    Subdivision("CF-LB", "Lobaye"),
    Subdivision("CF-MB", "Mbomou"),
    Subdivision("CF-MP", "Ombella-Mpoko"),
    Subdivision("CF-NM", "Nana-Mambéré"),
    Subdivision("CF-OP", "Ouham-Pendé"),
    Subdivision("CF-SE", "Sangha"),
    Subdivision("CF-UK", "Ouaka"),
    Subdivision("CF-VK", "Vakaga"),
]
