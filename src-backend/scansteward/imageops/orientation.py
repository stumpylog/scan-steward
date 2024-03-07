import logging
from pathlib import Path

from scansteward.imageops.metadata import bulk_read_image_metadata
from scansteward.imageops.metadata import bulk_write_image_metadata
from scansteward.imageops.metadata import read_image_metadata
from scansteward.imageops.metadata import write_image_metadata
from scansteward.imageops.models import ImageMetadata
from scansteward.imageops.models import RotationEnum

logger = logging.getLogger(__name__)


def read_image_rotation(image_path: Path) -> ImageMetadata:
    metadata = read_image_metadata(image_path, read_orientation=True)
    if not metadata.Orientation:
        logger.warn("No Orientation was read, assuming HORIZONTAL")
        metadata.Orientation = RotationEnum.HORIZONTAL
    return metadata


def bulk_read_image_rotation(images: list[Path]) -> list[ImageMetadata]:
    return bulk_read_image_metadata(images, read_orientation=True)


def write_image_rotation(metadata: ImageMetadata) -> None:
    return write_image_metadata(metadata)


def bulk_write_image_rotation(metadata: list[ImageMetadata]) -> None:
    return bulk_write_image_metadata(metadata)
