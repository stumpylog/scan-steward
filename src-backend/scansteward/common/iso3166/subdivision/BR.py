from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("BR-AC", "Acre"),
    Subdivision("BR-AL", "Alagoas"),
    Subdivision("BR-AM", "Amazonas"),
    Subdivision("BR-AP", "Amapá"),
    Subdivision("BR-BA", "Bahia"),
    Subdivision("BR-CE", "Ceará"),
    Subdivision("BR-DF", "Distrito Federal"),
    Subdivision("BR-ES", "Espírito Santo"),
    Subdivision("BR-GO", "Goiás"),
    Subdivision("BR-MA", "Maranhão"),
    Subdivision("BR-MG", "Minas Gerais"),
    Subdivision("BR-MS", "Mato Grosso do Sul"),
    Subdivision("BR-MT", "Mato Grosso"),
    Subdivision("BR-PA", "Pará"),
    Subdivision("BR-PB", "Paraíba"),
    Subdivision("BR-PE", "Pernambuco"),
    Subdivision("BR-PI", "Piauí"),
    Subdivision("BR-PR", "Paraná"),
    Subdivision("BR-RJ", "Rio de Janeiro"),
    Subdivision("BR-RN", "Rio Grande do Norte"),
    Subdivision("BR-RO", "Rondônia"),
    Subdivision("BR-RR", "Roraima"),
    Subdivision("BR-RS", "Rio Grande do Sul"),
    Subdivision("BR-SC", "Santa Catarina"),
    Subdivision("BR-SE", "Sergipe"),
    Subdivision("BR-SP", "São Paulo"),
    Subdivision("BR-TO", "Tocantins"),
]
