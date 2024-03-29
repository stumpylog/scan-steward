from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("MY-01", "Johor"),
    Subdivision("MY-02", "Kedah"),
    Subdivision("MY-03", "Kelantan"),
    Subdivision("MY-04", "Melaka"),
    Subdivision("MY-05", "Negeri Sembilan"),
    Subdivision("MY-06", "Pahang"),
    Subdivision("MY-07", "Pulau Pinang"),
    Subdivision("MY-08", "Perak"),
    Subdivision("MY-09", "Perlis"),
    Subdivision("MY-10", "Selangor"),
    Subdivision("MY-11", "Terengganu"),
    Subdivision("MY-12", "Sabah"),
    Subdivision("MY-13", "Sarawak"),
    Subdivision("MY-14", "Wilayah Persekutuan Kuala Lumpur"),
    Subdivision("MY-15", "Wilayah Persekutuan Labuan"),
    Subdivision("MY-16", "Wilayah Persekutuan Putrajaya"),
]
