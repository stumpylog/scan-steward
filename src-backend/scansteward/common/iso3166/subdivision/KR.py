from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("KR-11", "Seoul-teukbyeolsi"),
    Subdivision("KR-26", "Busan-gwangyeoksi"),
    Subdivision("KR-27", "Daegu-gwangyeoksi"),
    Subdivision("KR-28", "Incheon-gwangyeoksi"),
    Subdivision("KR-29", "Gwangju-gwangyeoksi"),
    Subdivision("KR-30", "Daejeon-gwangyeoksi"),
    Subdivision("KR-31", "Ulsan-gwangyeoksi"),
    Subdivision("KR-41", "Gyeonggi-do"),
    Subdivision("KR-42", "Gangwon-teukbyeoljachido"),
    Subdivision("KR-43", "Chungcheongbuk-do"),
    Subdivision("KR-44", "Chungcheongnam-do"),
    Subdivision("KR-45", "Jeollabuk-do"),
    Subdivision("KR-46", "Jeollanam-do"),
    Subdivision("KR-47", "Gyeongsangbuk-do"),
    Subdivision("KR-48", "Gyeongsangnam-do"),
    Subdivision("KR-49", "Jeju-teukbyeoljachido"),
    Subdivision("KR-50", "Sejong"),
]
