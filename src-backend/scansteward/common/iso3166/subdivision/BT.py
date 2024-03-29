from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("BT-11", "Paro"),
    Subdivision("BT-12", "Chhukha"),
    Subdivision("BT-13", "Haa"),
    Subdivision("BT-14", "Samtse"),
    Subdivision("BT-15", "Thimphu"),
    Subdivision("BT-21", "Tsirang"),
    Subdivision("BT-22", "Dagana"),
    Subdivision("BT-23", "Punakha"),
    Subdivision("BT-24", "Wangdue Phodrang"),
    Subdivision("BT-31", "Sarpang"),
    Subdivision("BT-32", "Trongsa"),
    Subdivision("BT-33", "Bumthang"),
    Subdivision("BT-34", "Zhemgang"),
    Subdivision("BT-41", "Trashigang"),
    Subdivision("BT-42", "Monggar"),
    Subdivision("BT-43", "Pema Gatshel"),
    Subdivision("BT-44", "Lhuentse"),
    Subdivision("BT-45", "Samdrup Jongkhar"),
    Subdivision("BT-GA", "Gasa"),
    Subdivision("BT-TY", "Trashi Yangtse"),
]
