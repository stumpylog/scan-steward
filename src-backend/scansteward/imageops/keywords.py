import logging
import subprocess
from pathlib import Path

from scansteward.imageops.constants import EXIF_TOOL_EXE
from scansteward.imageops.metadata import bulk_read_image_metadata
from scansteward.imageops.metadata import bulk_write_image_metadata
from scansteward.imageops.metadata import write_image_metadata
from scansteward.imageops.models import ImageMetadata

logger = logging.getLogger(__name__)


def read_keywords(image_path: Path) -> ImageMetadata:
    return bulk_read_keywords([image_path])[0]


def bulk_read_keywords(images: list[Path]) -> list[ImageMetadata]:
    return bulk_read_image_metadata(images, read_tags=True)


def bulk_clear_existing_keywords(images: list[Path]) -> None:
    cmd = [
        EXIF_TOOL_EXE,
        "-struct",
        "-json",
        "-n",  # Disable print conversion, use machine readable
        "-HierarchicalKeywords=",
        "-LastKeywordXMP=",
        "-TagsList=",
        "-HierarchicalSubject=",
        "-CatalogSets=",
    ]
    for image in images:
        cmd.append(str(image.resolve()))  # noqa: PERF401
    proc = subprocess.run(cmd, check=False, capture_output=True)
    if proc.returncode != 0:
        for line in proc.stderr.decode("utf-8").splitlines():
            logger.error(f"exiftool: {line}")
        for line in proc.stdout.decode("utf-8").splitlines():
            logger.info(f"exiftool : {line}")

    # Do this after logging anything
    proc.check_returncode()


def write_keywords(metadata: ImageMetadata, *, clear_existing: bool = False) -> None:
    if clear_existing:
        bulk_clear_existing_keywords([metadata.SourceFile])
    return write_image_metadata(metadata)


def bulk_write_image_keywords(metadata: list[ImageMetadata], *, clear_existing: bool = False) -> None:
    if clear_existing:
        bulk_clear_existing_keywords([x.SourceFile for x in metadata])
    return bulk_write_image_metadata(metadata)
