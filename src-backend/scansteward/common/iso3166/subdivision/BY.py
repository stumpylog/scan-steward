from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("BY-BR", "Bresckaja voblasć"),
    Subdivision("BY-HM", "Gorod Minsk"),
    Subdivision("BY-HO", "Gomel'skaja oblast'"),
    Subdivision("BY-HR", "Grodnenskaja oblast'"),
    Subdivision("BY-MA", "Mahilioŭskaja voblasć"),
    Subdivision("BY-MI", "Minskaja oblast'"),
    Subdivision("BY-VI", "Viciebskaja voblasć"),
]
