from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("GE-AB", "Abkhazia"),
    Subdivision("GE-AJ", "Ajaria"),
    Subdivision("GE-GU", "Guria"),
    Subdivision("GE-IM", "Imereti"),
    Subdivision("GE-KA", "K'akheti"),
    Subdivision("GE-KK", "Kvemo Kartli"),
    Subdivision("GE-MM", "Mtskheta-Mtianeti"),
    Subdivision("GE-RL", "Rach'a-Lechkhumi-Kvemo Svaneti"),
    Subdivision("GE-SJ", "Samtskhe-Javakheti"),
    Subdivision("GE-SK", "Shida Kartli"),
    Subdivision("GE-SZ", "Samegrelo-Zemo Svaneti"),
    Subdivision("GE-TB", "Tbilisi"),
]
