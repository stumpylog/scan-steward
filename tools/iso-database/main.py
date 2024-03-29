from pathlib import Path
from httpx import Client
import orjson as json
from collections import defaultdict

ISO_3166_1_JSON_URL = (
    "https://salsa.debian.org/iso-codes-team/iso-codes/-/raw/main/data/iso_3166-1.json"
)
ISO_3166_2_JSON_URL = (
    "https://salsa.debian.org/iso-codes-team/iso-codes/-/raw/main/data/iso_3166-2.json"
)

URLS = [ISO_3166_1_JSON_URL, ISO_3166_2_JSON_URL]


def main(
    data_dir: Path = Path(),
    module_dir: Path = Path("database"),
    *,
    force_update: bool = False,
):
    country_json = data_dir / "iso_3166-1.json"
    subdivision_json = data_dir / "iso_3166-2.json"
    for output_file, url in zip(
        [country_json, subdivision_json],
        URLS,
        strict=True,
    ):
        if force_update or not output_file.exists():
            with Client() as client:
                response = client.get(url)
                response.raise_for_status()
                output_file.write_bytes(response.content)

    if not module_dir.exists():
        module_dir.mkdir(parents=True, exist_ok=True)

    countries_dir = module_dir / "country"
    country_file = countries_dir / "countries.py"
    subdivision_dir = module_dir / "subdivision"

    if not countries_dir.exists():
        countries_dir.mkdir(parents=True, exist_ok=True)

    if not subdivision_dir.exists():
        subdivision_dir.mkdir(parents=True, exist_ok=True)

    with country_file.open("w", encoding="utf-8") as f:
        f.write("from typing import Final\n")
        f.write("from ..models import Country\n\n")
        f.write("ALPHA2_CODE_TO_COUNTRIES: Final[dict[str, Country]] = {\n")

        country_list = json.loads(country_json.read_text(encoding="utf-8"))["3166-1"]
        for country in country_list:
            name: str = country["name"]
            alpha2 = country["alpha_2"]
            f.write(f'    "{alpha2}": Country("{alpha2}", "{name}"),\n')
        f.write("}\n")

    subdivision_list = json.loads(subdivision_json.read_text(encoding="utf-8"))[
        "3166-2"
    ]

    country_code_to_subdivision: dict[str, list] = defaultdict(list)

    for subdivision in subdivision_list:
        subdivision_code: str = subdivision["code"]
        country_alpha_2 = subdivision_code.split("-")[0]
        country_code_to_subdivision[country_alpha_2].append(subdivision)

    for country_code in country_code_to_subdivision:
        with (subdivision_dir / f"{country_code.upper()}.py").open(
            "w", encoding="utf-8"
        ) as f:
            f.write("from typing import Final\n")
            f.write("from ..models import Subdivision\n\n")
            f.write("SUBDIVISIONS: Final[list[Subdivision]] = [\n")
            for subdivision in country_code_to_subdivision[country_code]:
                name: str = subdivision["name"]
                code = subdivision["code"]
                f.write(f'        Subdivision("{code}", "{name}"),\n')
            f.write("]\n")


if __name__ == "__main__":
    import typer

    typer.run(main)
