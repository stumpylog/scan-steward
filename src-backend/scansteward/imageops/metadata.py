import logging
import subprocess
import tempfile
from pathlib import Path

import orjson as json

from scansteward.imageops.constants import EXIF_TOOL_EXE
from scansteward.imageops.models import ImageMetadata
from scansteward.imageops.utils import now_string

logger = logging.getLogger(__name__)


def read_image_metadata(
    image_path: Path,
    *,
    read_regions: bool = False,
    read_orientation: bool = False,
    read_tags: bool = False,
) -> ImageMetadata:
    return bulk_read_image_metadata(
        [image_path],
        read_regions=read_regions,
        read_orientation=read_orientation,
        read_tags=read_tags,
    )[0]


def bulk_read_image_metadata(
    images: list[Path],
    *,
    read_regions: bool = False,
    read_orientation: bool = False,
    read_tags: bool = False,
) -> list[ImageMetadata]:

    # Something must be asked for
    if not any([read_regions, read_orientation, read_tags]):
        msg = "One of read_regions or read_orientation or read_tags is required"
        logger.error(msg)
        raise ValueError(msg)
    if not images:
        msg = "No image paths were provided"
        logger.error(msg)
        raise ValueError(msg)

    actual_images = []
    for image_path in images:
        if not image_path.exists():
            msg = f"{image_path} does not exist"
            logger.error(msg)
            raise FileExistsError(image_path)
        elif not image_path.is_file():
            msg = f"{image_path} is not a file"
            logger.error(msg)
            raise ValueError(msg)
        actual_images.append(image_path.resolve())

    cmd = [
        EXIF_TOOL_EXE,
        "-struct",
        "-json",
        "-n",  # Disable print conversion, use machine readable
    ]
    # Add the request for the requested flags
    if read_regions:
        cmd.append("-RegionInfo")
    if read_orientation:
        cmd.append("-Orientation")
    if read_tags:
        cmd.extend(
            ["-HierarchicalKeywords", "-LastKeywordXMP", "-TagsList", "-HierarchicalSubject", "-CatalogSets"],
        )
    # Add the actual images
    cmd.extend(actual_images)

    # And run the command
    proc = subprocess.run(cmd, check=False, capture_output=True)
    if proc.returncode != 0:
        for line in proc.stderr.decode("utf-8").splitlines():
            logger.error(f"exiftool: {line}")
    for line in proc.stdout.decode("utf-8").splitlines():
        logger.info(f"exiftool : {line}")

    # Do this after logging anything
    proc.check_returncode()
    return [ImageMetadata.model_validate(x) for x in json.loads(proc.stdout.decode("utf-8"))]


def write_image_metadata(metadata: ImageMetadata) -> None:
    return bulk_write_image_metadata([metadata])


def bulk_write_image_metadata(metadata: list[ImageMetadata]) -> None:
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
        proc = subprocess.run(cmd, check=False, capture_output=True)

        if proc.returncode != 0:
            for line in proc.stderr.decode("utf-8").splitlines():
                logger.error(f"exiftool: {line}")
        for line in proc.stdout.decode("utf-8").splitlines():
            logger.info(f"exiftool : {line}")

        proc.check_returncode()
