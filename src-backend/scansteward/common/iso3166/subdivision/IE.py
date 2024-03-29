from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("IE-C", "Connaught"),
    Subdivision("IE-CE", "Clare"),
    Subdivision("IE-CN", "Cavan"),
    Subdivision("IE-CO", "Cork"),
    Subdivision("IE-CW", "Carlow"),
    Subdivision("IE-D", "Dublin"),
    Subdivision("IE-DL", "Donegal"),
    Subdivision("IE-G", "Galway"),
    Subdivision("IE-KE", "Kildare"),
    Subdivision("IE-KK", "Kilkenny"),
    Subdivision("IE-KY", "Kerry"),
    Subdivision("IE-L", "Leinster"),
    Subdivision("IE-LD", "Longford"),
    Subdivision("IE-LH", "Louth"),
    Subdivision("IE-LK", "Limerick"),
    Subdivision("IE-LM", "Leitrim"),
    Subdivision("IE-LS", "Laois"),
    Subdivision("IE-M", "Munster"),
    Subdivision("IE-MH", "Meath"),
    Subdivision("IE-MN", "Monaghan"),
    Subdivision("IE-MO", "Mayo"),
    Subdivision("IE-OY", "Offaly"),
    Subdivision("IE-RN", "Roscommon"),
    Subdivision("IE-SO", "Sligo"),
    Subdivision("IE-TA", "Tipperary"),
    Subdivision("IE-U", "Ulster"),
    Subdivision("IE-WD", "Waterford"),
    Subdivision("IE-WH", "Westmeath"),
    Subdivision("IE-WW", "Wicklow"),
    Subdivision("IE-WX", "Wexford"),
]
