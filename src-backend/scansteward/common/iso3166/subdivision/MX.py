from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("MX-AGU", "Aguascalientes"),
    Subdivision("MX-BCN", "Baja California"),
    Subdivision("MX-BCS", "Baja California Sur"),
    Subdivision("MX-CAM", "Campeche"),
    Subdivision("MX-CHH", "Chihuahua"),
    Subdivision("MX-CHP", "Chiapas"),
    Subdivision("MX-CMX", "Ciudad de México"),
    Subdivision("MX-COA", "Coahuila de Zaragoza"),
    Subdivision("MX-COL", "Colima"),
    Subdivision("MX-DUR", "Durango"),
    Subdivision("MX-GRO", "Guerrero"),
    Subdivision("MX-GUA", "Guanajuato"),
    Subdivision("MX-HID", "Hidalgo"),
    Subdivision("MX-JAL", "Jalisco"),
    Subdivision("MX-MEX", "México"),
    Subdivision("MX-MIC", "Michoacán de Ocampo"),
    Subdivision("MX-MOR", "Morelos"),
    Subdivision("MX-NAY", "Nayarit"),
    Subdivision("MX-NLE", "Nuevo León"),
    Subdivision("MX-OAX", "Oaxaca"),
    Subdivision("MX-PUE", "Puebla"),
    Subdivision("MX-QUE", "Querétaro"),
    Subdivision("MX-ROO", "Quintana Roo"),
    Subdivision("MX-SIN", "Sinaloa"),
    Subdivision("MX-SLP", "San Luis Potosí"),
    Subdivision("MX-SON", "Sonora"),
    Subdivision("MX-TAB", "Tabasco"),
    Subdivision("MX-TAM", "Tamaulipas"),
    Subdivision("MX-TLA", "Tlaxcala"),
    Subdivision("MX-VER", "Veracruz de Ignacio de la Llave"),
    Subdivision("MX-YUC", "Yucatán"),
    Subdivision("MX-ZAC", "Zacatecas"),
]
