import subprocess
import tempfile
from pathlib import Path

import orjson as json

from scansteward.imageops.constants import EXIF_TOOL_EXE
from scansteward.imageops.types import ImageMetadata
from scansteward.imageops.types import RotationEnum


def get_image_rotation(image_path: Path) -> RotationEnum:
    proc = subprocess.run(
        [  # noqa: S603
            EXIF_TOOL_EXE,  # type: ignore
            "-struct",
            "-json",
            "-n",  # Disable print conversion, use machine readable
            "-Orientation",
            str(image_path.resolve()),
        ],
        check=True,
        capture_output=True,
    )
    data = json.loads(proc.stdout.decode("utf-8"))[0]
    return RotationEnum(data.get("Orientation", RotationEnum.HORIZONTAL))


def set_image_rotation(image_path: Path, rotation: RotationEnum) -> None:
    subprocess.run(
        [
            EXIF_TOOL_EXE,
            f"-Orientation={rotation.value}",
            "-n",
            str(image_path.resolve()),
        ],
        check=True,
    )


def set_image_rotation_bulk(metadata: list[ImageMetadata]) -> None:
    with tempfile.TemporaryDirectory() as json_dir:
        json_path = Path(json_dir).resolve() / "temp.json"
        data = [x.to_json() for x in metadata]
        img_files = [str(x.source_file.resolve() for x in metadata)]
        json_path.write_bytes(json.dumps(data))
        subprocess.run(
            [  # noqa: S603
                EXIF_TOOL_EXE,  # type: ignore
                "-overwrite_original",
                "-XMP:MetadataDate=now",
                "-n",  # Disable print conversion, use machine readable
                f"-json={json_path}",
                *img_files,
            ],
            check=False,
        )
