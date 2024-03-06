from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

import orjson as json

from scansteward.imageops.constants import EXIF_TOOL_EXE
from scansteward.imageops.types import RegionInfoStruct

if TYPE_CHECKING:
    from scansteward.imageops.types import ImageMetadata


def read_face_structs(image_path: Path) -> RegionInfoStruct | None:
    # exiftool -struct -json -xmp:all -n "2024-01-22-0006.jpg"
    proc = subprocess.run(
        [  # noqa: S603
            EXIF_TOOL_EXE,  # type: ignore
            "-struct",
            "-json",
            "-xmp:all",
            "-n",  # Disable print conversion, use machine readable
            str(image_path.resolve()),
        ],
        check=True,
        capture_output=True,
    )
    data = json.loads(proc.stdout.decode("utf-8"))[0]
    if "RegionInfo" not in data:
        return None
    return RegionInfoStruct.from_json(data["RegionInfo"])


def write_face_structs(metadata: ImageMetadata) -> None:
    with tempfile.TemporaryDirectory() as json_dir:
        json_path = Path(json_dir).resolve() / "temp.json"
        json_path.write_bytes(json.dumps(metadata.to_json()))
        subprocess.run(
            [  # noqa: S603
                EXIF_TOOL_EXE,  # type: ignore
                "-overwrite_original",
                "-XMP:MetadataDate=now",
                "-n",  # Disable print conversion, use machine readable
                "-writeMode",
                "cg",  # Create new tags/groups as necessary
                f"-json={json_path}",
                str(metadata.source_file.resolve()),
            ],
            check=False,
        )


def bulk_write_face_structs(metadata: list[ImageMetadata]) -> None:
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
                "-writeMode",
                "cg",  # Create new tags/groups as necessary
                f"-json={json_path}",
                *img_files,
            ],
            check=False,
        )
