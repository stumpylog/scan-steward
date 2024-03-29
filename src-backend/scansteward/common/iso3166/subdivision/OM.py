from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("OM-BJ", "Janūb al Bāţinah"),
    Subdivision("OM-BS", "Shamāl al Bāţinah"),
    Subdivision("OM-BU", "Al Buraymī"),
    Subdivision("OM-DA", "Ad Dākhilīyah"),
    Subdivision("OM-MA", "Masqaţ"),
    Subdivision("OM-MU", "Musandam"),
    Subdivision("OM-SJ", "Janūb ash Sharqīyah"),
    Subdivision("OM-SS", "Shamāl ash Sharqīyah"),
    Subdivision("OM-WU", "Al Wusţá"),
    Subdivision("OM-ZA", "Az̧ Z̧āhirah"),
    Subdivision("OM-ZU", "Z̧ufār"),
]
