from __future__ import annotations

import logging
import subprocess
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

import orjson as json

from scansteward.imageops.constants import EXIF_TOOL_EXE
from scansteward.imageops.models import RegionInfoStruct
from scansteward.imageops.utils import now_string

if TYPE_CHECKING:
    from scansteward.imageops.models import ImageMetadata

logger = logging.getLogger(__name__)


def read_face_structs(image_path: Path) -> RegionInfoStruct | None:
    # exiftool -struct -json -xmp:all -n "2024-01-22-0006.jpg"
    proc = subprocess.run(
        [
            EXIF_TOOL_EXE,  # type: ignore  # noqa: PGH003
            "-struct",
            "-json",
            "-n",  # Disable print conversion, use machine readable
            "-use MWG",
            "-RegionInfo",
            str(image_path.resolve()),
        ],
        check=True,
        capture_output=True,
    )
    data = json.loads(proc.stdout.decode("utf-8"))[0]
    if "RegionInfo" not in data:
        return None
    return RegionInfoStruct.model_validate(data["RegionInfo"])


def write_face_structs(metadata: ImageMetadata) -> None:
    with tempfile.TemporaryDirectory() as json_dir:
        json_path = Path(json_dir).resolve() / "temp.json"
        json_path.write_text(metadata.model_dump_json(exclude_none=True, exclude_unset=True))
        cmd = [
            EXIF_TOOL_EXE,
            "-overwrite_original",
            f"-ModifyDate={now_string()}",
            "-n",  # Disable print conversion, use machine readable
            "-writeMode",
            "wcg",  # Create new tags/groups as necessary
            f"-json={json_path}",
            str(metadata.SourceFile.resolve()),
        ]
        subprocess.run(cmd, check=True)


def bulk_write_face_structs(metadata: list[ImageMetadata]) -> None:
    with tempfile.TemporaryDirectory() as json_dir:
        json_path = Path(json_dir).resolve() / "temp.json"
        json_path.write_bytes(
            json.dumps([x.model_dump(exclude_none=True, exclude_unset=True) for x in metadata]),
        )
        cmd = [
            EXIF_TOOL_EXE,
            "-struct",
            "-n",  # Disable print conversion, use machine readable
            "-overwrite_original",
            f"-ModifyDate={now_string()}",
            "-writeMode",
            "wcg",  # Create new tags/groups as necessary, overwrite existing
            f"-json={json_path}",
        ]
        # * unpacking doesn't resolve for the command
        for x in metadata:
            cmd.append(x.SourceFile.resolve())  # noqa: PERF401
        proc = subprocess.run(cmd, check=False, capture_output=True)
        for line in proc.stderr.decode("utf-8").splitlines():
            logger.error(f"exiftool: {line}")
        for line in proc.stdout.decode("utf-8").splitlines():
            logger.info(f"exiftool: {line}")

        proc.check_returncode()
