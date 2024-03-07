import subprocess
import tempfile
from pathlib import Path

import orjson as json

from scansteward.imageops.constants import EXIF_TOOL_EXE
from scansteward.imageops.models import ImageMetadata
from scansteward.imageops.models import RotationEnum
from scansteward.imageops.utils import now_string


def read_image_rotation(image_path: Path) -> RotationEnum:
    proc = subprocess.run(
        [
            EXIF_TOOL_EXE,  # type: ignore
            "-struct",
            "-json",
            "-n",  # Disable print conversion, use machine readable
            "-use MWG",
            "-Orientation",
            str(image_path.resolve()),
        ],
        check=True,
        capture_output=True,
    )
    data = json.loads(proc.stdout.decode("utf-8"))[0]
    return RotationEnum(data.get("Orientation", RotationEnum.HORIZONTAL))


def write_image_rotation(metadata: ImageMetadata) -> None:
    with tempfile.TemporaryDirectory() as json_dir:
        json_path = Path(json_dir).resolve() / "temp.json"
        json_path.write_text(metadata.model_dump_json(exclude_none=True, exclude_unset=True))
        subprocess.run(
            [
                EXIF_TOOL_EXE,  # type: ignore
                "-overwrite_original",
                f"-ModifyDate={now_string()}",
                "-n",  # Disable print conversion, use machine readable
                f"-json={json_path}",
                str(metadata.SourceFile.resolve()),
            ],
            check=True,
        )


def bulk_write_image_rotation(metadata: list[ImageMetadata]) -> None:
    with tempfile.TemporaryDirectory() as json_dir:
        json_path = Path(json_dir).resolve() / "temp.json"
        data = [x.model_dump() for x in metadata]
        json_path.write_bytes(json.dumps(data))
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
        subprocess.run(cmd, check=True)
