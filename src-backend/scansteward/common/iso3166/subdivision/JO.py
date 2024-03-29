from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("JO-AJ", "‘Ajlūn"),
    Subdivision("JO-AM", "Al ‘A̅şimah"),
    Subdivision("JO-AQ", "Al ‘Aqabah"),
    Subdivision("JO-AT", "Aţ Ţafīlah"),
    Subdivision("JO-AZ", "Az Zarqā’"),
    Subdivision("JO-BA", "Al Balqā’"),
    Subdivision("JO-IR", "Irbid"),
    Subdivision("JO-JA", "Jarash"),
    Subdivision("JO-KA", "Al Karak"),
    Subdivision("JO-MA", "Al Mafraq"),
    Subdivision("JO-MD", "Mādabā"),
    Subdivision("JO-MN", "Ma‘ān"),
]
