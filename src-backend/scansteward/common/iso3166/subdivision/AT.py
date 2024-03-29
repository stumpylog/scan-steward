from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("AT-1", "Burgenland"),
    Subdivision("AT-2", "Kärnten"),
    Subdivision("AT-3", "Niederösterreich"),
    Subdivision("AT-4", "Oberösterreich"),
    Subdivision("AT-5", "Salzburg"),
    Subdivision("AT-6", "Steiermark"),
    Subdivision("AT-7", "Tirol"),
    Subdivision("AT-8", "Vorarlberg"),
    Subdivision("AT-9", "Wien"),
]
