from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("ZW-BU", "Bulawayo"),
    Subdivision("ZW-HA", "Harare"),
    Subdivision("ZW-MA", "Manicaland"),
    Subdivision("ZW-MC", "Mashonaland Central"),
    Subdivision("ZW-ME", "Mashonaland East"),
    Subdivision("ZW-MI", "Midlands"),
    Subdivision("ZW-MN", "Matabeleland North"),
    Subdivision("ZW-MS", "Matabeleland South"),
    Subdivision("ZW-MV", "Masvingo"),
    Subdivision("ZW-MW", "Mashonaland West"),
]
