from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("FI-01", "Landskapet Åland"),
    Subdivision("FI-02", "Etelä-Karjala"),
    Subdivision("FI-03", "Etelä-Pohjanmaa"),
    Subdivision("FI-04", "Etelä-Savo"),
    Subdivision("FI-05", "Kainuu"),
    Subdivision("FI-06", "Kanta-Häme"),
    Subdivision("FI-07", "Keski-Pohjanmaa"),
    Subdivision("FI-08", "Keski-Suomi"),
    Subdivision("FI-09", "Kymenlaakso"),
    Subdivision("FI-10", "Lappi"),
    Subdivision("FI-11", "Pirkanmaa"),
    Subdivision("FI-12", "Pohjanmaa"),
    Subdivision("FI-13", "Pohjois-Karjala"),
    Subdivision("FI-14", "Pohjois-Pohjanmaa"),
    Subdivision("FI-15", "Pohjois-Savo"),
    Subdivision("FI-16", "Päijät-Häme"),
    Subdivision("FI-17", "Satakunta"),
    Subdivision("FI-18", "Uusimaa"),
    Subdivision("FI-19", "Varsinais-Suomi"),
]
